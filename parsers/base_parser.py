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
    def parse(self, request: bytes) -> dict:
        """
        Parse request and return it as dictionary.
        :param request: Request to parse.
        :return: The parsed request as dictionary.
        """
        pass
