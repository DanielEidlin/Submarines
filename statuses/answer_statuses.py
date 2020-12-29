from enum import Enum, auto


class AnswerStatus(Enum):
    """
    Class representing an ANSWER request status.
    """
    CORRECT = auto()
    INCORRECT = auto()
    FULL_SUB_CORRECT = auto()
    VICTORY = auto()
