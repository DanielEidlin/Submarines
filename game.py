from parsers.base_parser import BaseParser
from requests.ready_request import ReadyRequest
from network_handlers.base_network_handler import BaseNetworkHandler

VERTICAL = "Vertical"
HORIZONTAL = "Horizontal"
BOARD_SIZE = 10
MINIMUM_POINT = 0
WATER = 0
SUBMARINE_PART = 1
DROWNED_SUBMARINE_PART = 2
SUBMARINE_LENGTHS = [5, 4, 3, 3, 2]


class Game:
    """
    Class representing a submarines game.
    """

    def __init__(self, network_handler: BaseNetworkHandler, parser: BaseParser):
        """
        Default constructor.
        :param network_handler: A NetworkHandler object for sending and receiving requests.
        :param parser: A Parser object for packing and parsing requests.
        """
        self.network_handler = network_handler
        self.parser = parser
        self.board = [[0] * 10] * 10

    def set_submarine_horizontally(self, start_column: int, end_column: int, row: int):
        """
        Sets a submarine on the board horizontally according to the coordinates specified.
        :param start_column: Start column of the submarine location.
        :param end_column: End column of the submarine location.
        :param row: Row of the submarine location.
        """
        for i in range(start_column, end_column + 1):
            self.board[row][i] = SUBMARINE_PART

    def set_submarine_vertically(self, start_row: int, end_row: int, column: int):
        """
        Sets a submarine on the board vertically according to the coordinates specified.
        :param start_row: Start row of the submarine location.
        :param end_row: End row of the submarine location.
        :param column: Column of the submarine location.
        """
        for i in range(start_row, end_row + 1):
            self.board[i][column] = SUBMARINE_PART

    def set_submarine(self, alignment: str, axis_value: int, start_point: int, end_point: int):
        """
        Sets the submarine on the board according to the parameters provided.
        :param alignment: Submarine alignment.
        :param axis_value: Value of the axis the submarine will be locate on.
        For example, a value of 5 with a horizontal alignment would be on the fifth row.
        :param start_point: Start point on the axis of the submarine's location.
        :param end_point: End point on the axis of the submarine's location.
        """
        if alignment == HORIZONTAL:
            self.set_submarine_horizontally(start_point, end_point, row=axis_value)
        else:
            self.set_submarine_vertically(start_point, end_point, column=axis_value)

    def validate_horizontal_location(self, start_column: int, end_column: int, row: int) -> bool:
        """
        Check if horizontally aligned submarine location is valid.
        :param start_column: Start column of the submarine location.
        :param end_column: End column of the submarine location.
        :param row: Row of the submarine location.
        :return: True if submarine location is valid.
        """
        for i in range(start_column, end_column):
            if self.board[row][i] == SUBMARINE_PART:
                return False
        return True

    def validate_vertical_location(self, start_row: int, end_row: int, column: int) -> bool:
        """
        Sets a submarine on the board vertically according to the coordinates specified.
        :param start_row: Start row of the submarine location.
        :param end_row: End row of the submarine location.
        :param column: Column of the submarine location.
        :return: True if submarine location is valid.
        """
        for i in range(start_row, end_row):
            if self.board[i][column] == SUBMARINE_PART:
                return False
        return True

    def is_location_valid(self, submarine_length: int, axis_value: int, alignment: str, start_point: int,
                          end_point: int) -> bool:
        """
        Check if submarine location is valid.
        :param submarine_length: Submarine length.
        :param axis_value: axis_value: Value of the axis the submarine will be locate on.
        For example, a value of 5 with a horizontal alignment would be on the fifth row.
        :param alignment: Submarine alignment.
        :param start_point: Start point on the axis of the submarine's location.
        :param end_point: End point on the axis of the submarine's location.
        :return: True if submarine location is valid.
        """
        if start_point >= BOARD_SIZE or start_point < MINIMUM_POINT:
            return False
        if end_point >= BOARD_SIZE or end_point < MINIMUM_POINT:
            return False
        if axis_value >= BOARD_SIZE or axis_value < MINIMUM_POINT:
            return False
        if abs(end_point - start_point) != submarine_length:
            return False
        if alignment == HORIZONTAL:
            return self.validate_horizontal_location(axis_value, start_point, end_point)
        elif alignment == VERTICAL:
            return self.validate_vertical_location(axis_value, start_point, end_point)
        return False

    def set_submarines(self):
        """
        Set submarines' locations.
        """
        for submarine_length in SUBMARINE_LENGTHS:
            alignment, axis_value, start_point, end_point = prompt_submarine_location()
            while not self.is_location_valid(submarine_length, axis_value, alignment, start_point, end_point):
                alignment, axis_value, start_point, end_point = prompt_submarine_location()
            self.set_submarine(alignment, axis_value, start_point, end_point)

    def initialize_connection(self):
        """
        Initialize a connection with an opponent.
        """
        if prompt_is_host():
            self.network_handler.listen()
        opponent_ip = prompt_opponent_ip()
        self.network_handler.connect(opponent_ip)

    def send_ready(self):
        """
        Send READY request to opponent.
        """
        data = self.parser.pack(ReadyRequest().to_dict())
        self.network_handler.send(data)

    def play(self):
        """
        Plays the game.
        """
        self.initialize_connection()
        self.set_submarines()
        self.send_ready()
