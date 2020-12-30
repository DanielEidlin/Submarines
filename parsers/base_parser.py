from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    Class representing an abstract parser.
    """
    @abstractmethod
    def pack(self, request: dict) -> bytes:
        """
        Pack request and return it as bytes.
        :param request: Request to pack.
        :return: The packed request as bytes.
        """
        pass

    @abstractmethod
    def parse(self, data: bytes) -> dict:
        """
        Parse request and return it as dictionary.
        :param data: Data to parse.
        :return: The parsed request as dictionary.
        """
        pass
