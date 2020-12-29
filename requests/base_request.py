from abc import ABC, abstractmethod


class BaseRequest(ABC):
    """
    Class representing an abstract request.
    """

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Returns the request as a dictionary.
        :return: The request as dictionary.
        """
        pass
