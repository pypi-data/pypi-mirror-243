from http.client import RemoteDisconnected
import random
import re
import requests
from parsel import Selector
from time import sleep
from urllib.error import ContentTooShortError, URLError
import traceback

NETWORK_ERRORS = [RemoteDisconnected, URLError,
                  ConnectionAbortedError, ContentTooShortError, BlockingIOError]


def istuple(el):
    return type(el) is tuple


def is_errors_instance(instances, error):
    for i in range(len(instances)):
        ins = instances[i]
        if isinstance(error, ins):
            return True, i
    return False, -1


def retry_if_is_error(func, instances=None, retries=2, initial_wait_time=1, log_error=True):
    tries = 0
    wait_time = initial_wait_time

    while tries < retries:
        try:
            return func()
        except Exception as e:
            tries += 1
            is_valid_error, index = is_errors_instance(
                [ex[0] if isinstance(ex, tuple) else ex for ex in instances], e)

            if not is_valid_error:
                raise

            if log_error:
                print(f'Attempt {tries} failed: {e}')

            if tries < retries:
                sleep(wait_time)
                wait_time *= 2  # Raddoppia il tempo di attesa per ogni tentativo fallito

    print(f'Operation failed after {retries} retries.')
    return None



def extract_links_from_html(html):
    selector = Selector(text=html)
    links = []

    for a in selector.xpath("//a[@href]"):
        href = a.xpath("@href").get()
        if 'http' in href:
            links.append(href)

    return links


def extract_links_from_text(text):
    result = re.search("(?P<url>https?://[^\s]+)", text).group("url")
    return [result]


API = 'https://www.1secmail.com/api/v1/'


def extractids(req):
    id_list = []
    for i in req:
        for k, v in i.items():
            if k == 'id':
                mail_id = v
                id_list.append(mail_id)
    return id_list


domainList = None


def get_domains():
    global domainList
    if domainList is None:
        domainList = requests.get(
            "https://www.1secmail.com/api/v1/?action=getDomainList").json()
    return domainList


class TempMail:

    @staticmethod
    def generate_email(username):
        # ['1secmail.com', '1secmail.net', '1secmail.org']
        domain = random.choice(get_domains())

        email = f'{username}@{domain}'
        return email

    @staticmethod
    def extract(email: str):
        ls = email.split('@')
        login = ls[0]
        domain = ls[1]
        return login, domain

    @staticmethod
    def delete_mailbox(email):
        login, domain = TempMail.extract(email)
        url = 'https://www.1secmail.com/mailbox'
        data = {
            'action': 'deleteMailbox',
            'login': f'{login}',
            'domain': f'{domain}'
        }

        requests.post(url, data=data)

    @staticmethod
    def get_domains():
        return get_domains()

    @staticmethod
    def get_email_link(email):
        def run():
            login, domain = TempMail.extract(email)
            req_link = f'{API}?action=getMessages&login={login}&domain={domain}'
            req = requests.get(req_link).json()

            if not req:
                raise Exception("No Emails Found")  # Solleva un'eccezione invece di restituire un messaggio

            _id = extractids(req)[-1]

            msg_read = f'{API}?action=readMessage&login={login}&domain={domain}&id={_id}'
            req = requests.get(msg_read).json()

            html = req['htmlBody']
            links = extract_links_from_html(html) if html else extract_links_from_text(req['textBody'])

            if not links:
                raise Exception("No Links Found")  # Solleva un'eccezione anche qui

            return links[0]

        result = retry_if_is_error(
            run, NETWORK_ERRORS + [Exception], 5, 5, True)
        return result

    @staticmethod
    def get_body(email):
        def run():
            login, domain = TempMail.extract(email)
            req_link = f'{API}?action=getMessages&login={login}&domain={domain}'
            req = requests.get(req_link).json()

            if len(req) == 0:
                assert False, "No Emails"

            _id = extractids(req)[-1]

            msg_read = f'{API}?action=readMessage&login={login}&domain={domain}&id={_id}'
            req = requests.get(msg_read).json()

            html = req['htmlBody']

            if html == '':
                return req['textBody']
            else:
                return html

        retry_if_is_error(run, NETWORK_ERRORS + [AssertionError], 5, 5, False)
        data = run()
        return data

    @staticmethod
    def get_email_link_and_delete_mailbox(email):
        return_link = TempMail.get_email_link(email)
        TempMail.delete_mailbox(email)
        return return_link


if __name__ == '__main__':
    link = TempMail.get_email_link("stealbot@1secmail.com")
    print(link)
