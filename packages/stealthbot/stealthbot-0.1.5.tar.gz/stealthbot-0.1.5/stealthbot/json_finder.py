import re
import json


class _JsonFinder(object):
    def search(self, selector, fields):
        # Loop over all script tags to find matching JSON
        scripts = selector.css('script::text')
        for script in scripts:
            script_text = script.extract()
            script_text.replace(r'\n', ' ')
            brackets = self.bracketFinder(script_text)
            for bracket in brackets:
                if bracket:
                    try:
                        decoded_bracket = json.loads(bracket)
                        if self.containsFields(decoded_bracket, fields):
                            return decoded_bracket
                    except:
                        pass

    def containsFields(self, response, fields):
        """Returns True if json, or any nested json, contains fields"""
        return all([self.containsField(response, field) for field in fields])

    def containsField(self, response, field):
        """Returns True if json, or any nested json, contains field"""
        return field in response or \
            any([self.containsField(subResponse, field)
                 for subResponse in response.values()
                 if type(subResponse) == dict])

    def bracketFinder(self, string):
        """Scan string for brackets and return contents."""
        numBrackets = 0
        startIndices = []
        endIndices = []
        for idx, char in enumerate(string):
            if char == '{':
                if numBrackets == 0:
                    startIndices.append(idx)
                numBrackets += 1
            elif char == '}':
                if numBrackets == 1:
                    endIndices.append(idx)
                numBrackets -= 1

        return [string[startIndex:endIndex + 1] for startIndex, endIndex
                in zip(startIndices, endIndices)]


JsonFinder = _JsonFinder()

