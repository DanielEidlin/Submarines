HORIZONTAL = "Horizontal"
BOARD_SIZE = 10
WATER = 0
SUBMARINE_PART = 1
DROWNED_SUBMARINE_PART = 2
SUBMARINE_LENGTHS = [5, 4, 3, 3, 2]


class Game:
    """
    Class representing a submarines game.
    """

    def __init__(self):
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
        :param start_point:
        :param end_point:
        :return:
        """
        if alignment == HORIZONTAL:
            self.set_submarine_horizontally(start_point, end_point, row=axis_value)
        else:
            self.set_submarine_vertically(start_point, end_point, column=axis_value)

    def set_submarines(self):
        """
        Set submarines' locations.
        """
        for submarine_length in SUBMARINE_LENGTHS:
            alignment, axis_value, start_point, end_point = prompt_submarine_location()
            while not is_submarine_location_valid(submarine_length, axis_value, alignment, start_point, end_point):
                alignment, axis_value, start_point, end_point = prompt_submarine_location()
            self.set_submarine(alignment, axis_value, start_point, end_point)

    def play(self, opponent_ip: str):
        """
        Plays the game.
        :param opponent_ip: The IP address of the opponent.
        """
        self.set_submarines()
