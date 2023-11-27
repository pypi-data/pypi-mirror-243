"""StealthBot: Un bot Python con tecnologia antidetect.

Questo modulo fornisce funzionalità per automatizzare compiti mantenendo
un profilo basso e evitando rilevazioni. È ideale per operazioni che richiedono
discrezione e sofisticatezza nell'elusione dei sistemi di rilevamento.
"""
__version__ = "0.1.5"

from .decorators import RetryException, stealth, request, AsyncQueueResult, AsyncResult
from .anti_detect_driver import StealthDriver
from .anti_detect_requests import StealthDriverRequests
import stealthbot.st as st


class StealthBot:
    def __init__(self):
        self.st = st
        self.stealth = stealth
        self.request = request
        self.RetryException = RetryException
        self.StealthDriver = StealthDriver
        self.AntiDetectRequests = StealthDriverRequests
        self.AsyncQueueResult = AsyncQueueResult
        self.AsyncResult = AsyncResult
