from .consts import REQUIRED_FIELDS
from .base_request import BaseRequest


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
