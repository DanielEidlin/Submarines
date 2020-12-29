from enum import Enum, auto


class ErrorStatus(Enum):
    """
    Class representing an ERROR request status.
    """
    OUT_OF_RANGE = auto()
    ATTEMPT_NOT_IN_TURN = auto()
    CLOSED = auto()
    UNEXPECTED = auto()
