import json

from base_parser import BaseParser

UNDERSCORE = "_"
MINUS_SIGN = "-"


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
            request[key] = value.replace(UNDERSCORE, MINUS_SIGN)
        return json.dumps(request).encode('utf-8')

    def parse(self, data: bytes) -> dict:
        """
        Parse request and return it as dictionary.
        :param data: Data to parse.
        :return: The parsed request as dictionary.
        """
        request = json.loads(data.decode('utf-8'))
        for key, value in request.items():
            request[key] = value.replace(MINUS_SIGN, UNDERSCORE)
        return request
