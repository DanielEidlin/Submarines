from .consts import REQUIRED_FIELDS
from .base_request import BaseRequest


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
