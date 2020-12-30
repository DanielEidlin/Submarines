import json

from .base_parser import BaseParser

SEPARATOR = ','
UNDERSCORE = "_"
MINUS_SIGN = "-"
REQUEST_SUFFIX = "\n\n"


class JSONParser(BaseParser):
    """
    Class representing a JSON parer.
    """

    def pack(self, request: dict) -> bytes:
        """
        Pack request and return it as bytes.
        :param request: Request to pack.
        :return: The packed request as bytes.
        """
        for key, value in request.items():
            if type(value) == list:
                request[key] = SEPARATOR.join(value)
            if type(value) == str:
                request[key] = value.replace(UNDERSCORE, MINUS_SIGN)
        return f"{json.dumps(request)}{REQUEST_SUFFIX}".encode('utf-8')

    def parse(self, data: bytes) -> dict:
        """
        Parse request and return it as dictionary.
        :param data: Data to parse.
        :return: The parsed request as dictionary.
        """
        request = json.loads(data.decode('utf-8'))
        for key, value in request.items():
            if type(value) == str:
                request[key] = value.replace(MINUS_SIGN, UNDERSCORE)
                if SEPARATOR in value:
                    request[key] = value.split(SEPARATOR)
        return request
