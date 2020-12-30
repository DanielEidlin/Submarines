from .consts import REQUIRED_FIELDS
from .base_request import BaseRequest
from statuses.answer_statuses import AnswerStatus


class AnswerRequest(BaseRequest):
    """
    Class representing an ANSWER request.
    """

    def __init__(self, statuses: list[AnswerStatus], x_coordinate: int = None, y_coordinate: int = None):
        """
        Default constructor.
        :param statuses: Answer request statuses.
        :param x_coordinate: X coordinate of the attempt.
        :param y_coordinate: Y coordinate of the attempt.
        """
        self.statuses = [status.name for status in statuses]
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def to_dict(self) -> dict:
        """
        Returns the request as a dictionary.
        :return: The request as dictionary.
        """
        if self.x_coordinate and self.y_coordinate:
            return dict(REQUIRED_FIELDS, **{"TYPE": "ANSWER"},
                        **{"X-COOR": self.x_coordinate, "Y-COOR": self.y_coordinate}, **{"STATUS": self.statuses})
        return dict(REQUIRED_FIELDS, **{"TYPE": "ANSWER"}, **{"STATUS": self.statuses})
