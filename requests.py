from abc import ABC, abstractmethod

VERSION = 1.0

REQUIRED_FIELDS = {
    "VERSION": VERSION,
    "TYPE": None
}


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


class ReadyRequest(BaseRequest):
    """
    Class representing a READY request.
    """

    def to_dict(self) -> dict:
        """
        Returns the request as a dictionary.
        :return: The request as dictionary.
        """
        return dict(REQUIRED_FIELDS, **{"TYPE": "READY"})


class AttemptRequest(BaseRequest):
    """
    Class representing an ATTEMPT request.
    """

    def __init__(self, x_coordinate: int, y_coordinate: int):
        """
        Default constructor.
        :param x_coordinate: X coordinate of the attempt.
        :param y_coordinate: Y coordinate of the attempt.
        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def to_dict(self) -> dict:
        """
        Returns the request as a dictionary.
        :return: The request as dictionary.
        """
        return dict(REQUIRED_FIELDS, **{"TYPE": "ATTEMPT"},
                    **{"X-COOR": self.x_coordinate, "Y-COOR": self.y_coordinate})


class AnswerRequest(BaseRequest):
    """
    Class representing an ANSWER request.
    """

    def __init__(self, x_coordinate: int, y_coordinate: int, status: Status):
        """
        Default constructor.
        :param x_coordinate: X coordinate of the attempt.
        :param y_coordinate: Y coordinate of the attempt.
        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.status = status

    def to_dict(self) -> dict:
        """
        Returns the request as a dictionary.
        :return: The request as dictionary.
        """
        return dict(REQUIRED_FIELDS, **{"TYPE": "ANSWER"},
                    **{"X-COOR": self.x_coordinate, "Y-COOR": self.y_coordinate}, **{"STATUS": self.status.name})
