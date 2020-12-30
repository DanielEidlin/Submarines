from parsers.base_parser import BaseParser
from requests.ready_request import ReadyRequest
from statuses.answer_statuses import AnswerStatus
from requests.answer_request import AnswerRequest
from requests.attempt_request import AttemptRequest
from validators.ready_validator import ReadyValidator
from validators.answer_validator import AnswerValidator
from validators.attempt_validator import AttemptValidator
from network_handlers.base_network_handler import BaseNetworkHandler

VERTICAL = "Vertical"
HORIZONTAL = "Horizontal"
BOARD_SIZE = 10
MINIMUM_POINT = 0
WATER = 0
SUBMARINE_PART = 1
DROWNED_SUBMARINE_PART = 2
SUBMARINE_LENGTHS = [5, 4, 3, 3, 2]
READY_TIMEOUT = 0.1


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
        self.is_starting = None

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

    def is_opponent_ready(self, timeout: float = None) -> bool:
        data = self.network_handler.receive(timeout=timeout)
        if not data:
            return False
        request = self.parser.parse(data)
        return ReadyValidator(request, self.network_handler, self.parser).is_valid()

    def send_ready(self):
        """
        Send READY request to opponent.
        """
        self.is_starting = not self.is_opponent_ready(timeout=READY_TIMEOUT)
        data = self.parser.pack(ReadyRequest().to_dict())
        self.network_handler.send(data)

    def initialize_game(self):
        self.initialize_connection()
        self.set_submarines()
        self.send_ready()
        if not self.is_starting:
            self.is_opponent_ready()

    def receive_request(self):
        data = self.network_handler.receive()
        return self.parser.parse(data)

    def send_guess(self):
        x_coordinate, y_coordinate = prompt_guess()
        request = AttemptRequest(x_coordinate, y_coordinate)
        data = self.parser.pack(request.to_dict())
        self.network_handler.send(data)

    def attempt_to_guess(self):
        self.send_guess()
        request = self.receive_request()
        is_answer_valid = AnswerValidator(request, self.network_handler, self.parser).is_valid()

        while not is_answer_valid:
            request = self.receive_request()
            is_answer_valid = AnswerValidator(request, self.network_handler, self.parser).is_valid()
        print_answer(request["STATUS"])

    def is_victory(self) -> bool:
        return any(SUBMARINE_PART in row for row in self.board)

    def is_full_sub(self, x_coordinate: int, y_coordinate: int) -> bool:
        for i in range(max(SUBMARINE_LENGTHS) - 1):
            right_cell = self.board[y_coordinate][x_coordinate + i]
            left_cell = self.board[y_coordinate][x_coordinate - i]
            bottom_cell = self.board[y_coordinate + i][x_coordinate]
            top_cell = self.board[y_coordinate - i][x_coordinate]
            if SUBMARINE_PART in [right_cell, left_cell, bottom_cell, top_cell]:
                return False
        return True

    def send_answer(self, answer_statuses: list[AnswerStatus], x_coordinate: int, y_coordinate: int):
        request = AnswerRequest(answer_statuses, x_coordinate, y_coordinate)
        data = self.parser.pack(request.to_dict())
        self.network_handler.send(data)

    def handle_guess(self, x_coordinate: int, y_coordinate: int):
        answer_statuses = []
        if self.board[y_coordinate][x_coordinate] == SUBMARINE_PART:
            self.board[y_coordinate][x_coordinate] = DROWNED_SUBMARINE_PART
            if self.is_victory():
                answer_statuses.append(AnswerStatus.VICTORY)
            if self.is_full_sub(x_coordinate, y_coordinate):
                answer_statuses.append(AnswerStatus.FULL_SUB_CORRECT)
            answer_statuses.append(AnswerStatus.CORRECT)
        answer_statuses.append(AnswerStatus.INCORRECT)
        self.send_answer(answer_statuses, x_coordinate, y_coordinate)

    def handle_opponent_attempt(self):
        request = self.receive_request()
        is_guess_valid = AttemptValidator(request, self.network_handler, self.parser).is_valid()

        while not is_guess_valid:
            request = self.receive_request()
            is_guess_valid = AttemptValidator(request, self.network_handler, self.parser).is_valid()
        handle_guess(request["X-COOR"], request["Y-COOR"])

    def start_game_loop(self):
        if self.is_starting:
            self.attempt_to_guess()

        while not self.is_victory():
            self.handle_opponent_attempt()
            self.attempt_to_guess()

    def play(self):
        """
        Plays the game.
        """
        # TODO: Handle ClosedException.
        self.initialize_game()
        self.start_game_loop()
