from .consts import REQUIRED_FIELDS
from .base_request import BaseRequest
from statuses.error_statuses import ErrorStatus


class ErrorRequest(BaseRequest):
    """
    Class representing an ERROR request.
    """

    def __init__(self, status: ErrorStatus):
        """
        Default constructor.
        :param status: Error request status.
        """
        self.status = status

    def to_dict(self) -> dict:
        """
        Returns the request as a dictionary.
        :return: The request as dictionary.
        """
        return dict(REQUIRED_FIELDS, **{"TYPE": "ERROR"}, **{"STATUS": self.status.name})
