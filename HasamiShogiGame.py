# Author: Holden Chen
# Date: 12/03/2021
# Description: Program defines a class called HasamiShogiGame, which represents an abstract board game played
# on a 9X9 board. The rules are: (1) Two players (Black and Red) each start with 9 nine pieces, arranged
# opposite to each other across the first (top) and last (bottom) rows; (2) Black moves first and then players
# alternate turns; (3) captures are made using the custodian capture rule; (3) pieces can only move horizontally
# or vertically; (5) the first player to capture 8 or more of their opponent's pieces wins the game.


class HasamiShogiGame:
    """
    Class representing a game of Hasami Shogi (variant 1). Responsibilities include:
    returning the status of the game, returning the active player for the current
    move, returning the num of captured pieces, making a move for a player, making
    captures, and returning/setting the occupant of a square.
    """

    def __init__(self):
        """
        Constructor method that creates a HasamiShogiGame object. Takes no parameters. The data members
        are _game_board, _game_state, _active_player, and _num_captured_pieces. 'RED' pieces start in row
        a of the _game_board and the 'BLACK' pieces start in row i. All other spaces are initialized to
        "NONE".
        """
        self._game_board = [
            ["RED", "RED", "RED", "RED", "RED", "RED", "RED", "RED", "RED"],
            ["NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"],
            ["NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"],
            ["NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"],
            ["NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"],
            ["NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"],
            ["NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"],
            ["NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", "NONE"],
            ["BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK", "BLACK"]
        ]

        self._game_state = "UNFINISHED"  # _game_state is either "UNFINISHED", "RED_WON", or "BLACK_WON"
        self._active_player = "BLACK"  # "BLACK" moves first, then the players alternate turns
        self._num_captured_pieces = {"BLACK": 0, "RED": 0}  # number of pieces of that color that have been captured

    def get_game_state(self):
        """
        Takes no parameters and returns the state of the game - either 'UNFINISHED', 'RED_WON'
        or 'BLACK_WON'.
        """
        return self._game_state

    def get_active_player(self):
        """
        Takes no parameters and returns whose turn it is - either 'RED' or 'BLACK'.
        """
        return self._active_player

    def get_num_captured_pieces(self, player_color):
        """
        Takes one parameter, 'RED' or 'BLACK', and returns the number of pieces of that color that
        have been captured.
        """
        try:
            player_color.upper()
            if player_color not in self._num_captured_pieces:
                return "Invalid entry. Please enter either 'RED' or 'BLACK'."

            return self._num_captured_pieces[player_color]
        except SyntaxError or AttributeError:
            print("Invalid entry. Please enter either 'RED' or 'BLACK'.")

    def convert_algebraic_notation(self, location):
        """
        Takes one parameter - a square location in algebraic notation. It returns a list
        containing the corresponding row index as the first element and the corresponding column
        index as the second element.
        """
        row_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        row_index = row_letters.index(location[0].lower())
        if len(location) != 2:
            print("Invalid input. Please try again")

        column_index = int(location[1]) - 1
        return [row_index, column_index]

    def validate_move(self, from_location, to_location):
        """
        Takes two parameters – the location of a square to move from (from_square) and the location of
        a square to move to (to_square). Both should be strings in algebraic notation. If the square
        being moved from does not contain a piece belonging to the player whose turn it is, or if the
        indicated move is not legal, or if the game has already been won, it returns False. Otherwise,
        it returns True so that the player can proceed with the move.
        """
        from_square_row_index = self.convert_algebraic_notation(from_location)[0]
        from_square_col_index = self.convert_algebraic_notation(from_location)[1]
        to_square_row_index = self.convert_algebraic_notation(to_location)[0]
        to_square_col_index = self.convert_algebraic_notation(to_location)[1]

        if self._game_board[from_square_row_index][from_square_col_index] not in self._active_player:
            return False
        if "UNFINISHED" not in self._game_state:
            return False

        if to_location in from_location:
            return False
        if "NONE" not in self._game_board[to_square_row_index][to_square_col_index]:
            return False
        if from_square_row_index != to_square_row_index and from_square_col_index != to_square_col_index:
            return False

        # check for pieces between from_square and to_square when move is vertical
        if from_square_row_index > to_square_row_index and from_square_col_index == to_square_col_index:
            for temp_row_index in range(to_square_row_index + 1, from_square_row_index):
                if "NONE" not in self._game_board[temp_row_index][from_square_col_index]:
                    return False
                else:
                    continue
            return True
        if from_square_row_index < to_square_row_index and from_square_col_index == to_square_col_index:
            for temp_row_index in range(from_square_row_index + 1, to_square_row_index):
                if "NONE" not in self._game_board[temp_row_index][from_square_col_index]:
                    return False
                else:
                    continue
            return True

        # check for pieces between from_square and to_square when move is horizontal
        if from_square_row_index == to_square_row_index and from_square_col_index > to_square_col_index:
            for temp_col_index in range(to_square_col_index + 1, from_square_col_index):
                if "NONE" not in self._game_board[from_square_row_index][temp_col_index]:
                    return False
                else:
                    continue
            return True
        if from_square_row_index == to_square_row_index and from_square_col_index < to_square_col_index:
            for temp_col_index in range(from_square_col_index + 1, to_square_col_index):
                if "NONE" not in self._game_board[from_square_row_index][temp_col_index]:
                    return False
                else:
                    continue
            return True

    def capture_pieces_above(self, row_index, col_index):
        """
        Takes two parameters - the row index and the column index of a square, and checks
        for captures that exist above the square. If there is a capture, then the method will remove
        the captured pieces and update the number captured for the color of the pieces captured.
        """
        if row_index < 0:
            return
        elif row_index - 1 >= 0:
            if "NONE" in self._game_board[row_index - 1][col_index]:
                return

        square_occupant = self._game_board[row_index][col_index]

        # CHECK CORNER CAPTURE
        if row_index == 0 and col_index == 0:
            right_occupant = self._game_board[row_index][col_index + 1]
            if self._active_player in right_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1
        elif row_index == 0 and col_index == 8:
            left_occupant = self._game_board[row_index][col_index - 1]
            if self._active_player in left_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1

        if self._active_player in square_occupant:
            return
        elif "NONE" in square_occupant:
            return

        self.capture_pieces_above(row_index - 1, col_index)  # recursive call

        if row_index - 1 < 0:
            return
        elif self._active_player in square_occupant or "NONE" in square_occupant:
            return
        elif self._active_player not in self._game_board[row_index-1][col_index]:
            if "NONE" not in self._game_board[row_index - 1][col_index]:
                return

        captured_piece = self._game_board[row_index][col_index]
        self._num_captured_pieces[captured_piece] += 1
        self._game_board[row_index][col_index] = "NONE"

    def capture_pieces_below(self, row_index, col_index):
        """
        Takes two parameters - the row index and the column index of a square, and checks
        for captures that exist below the given square. If there is a capture, then the method will
        remove the captured pieces and update the number captured for the color of the pieces captured.
        """
        if row_index > 8:
            return
        elif row_index + 1 <= 8:
            if "NONE" in self._game_board[row_index + 1][col_index]:
                return

        square_occupant = self._game_board[row_index][col_index]

        # CHECK CORNER CAPTURES
        if row_index == 8 and col_index == 0:
            right_occupant = self._game_board[row_index][col_index + 1]
            if self._active_player in right_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1
        elif row_index == 8 and col_index == 8:
            left_occupant = self._game_board[row_index][col_index - 1]
            if self._active_player in left_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1

        if self._active_player in square_occupant:
            return
        elif "NONE" in square_occupant:
            return

        self.capture_pieces_below(row_index + 1, col_index)  # recursive call

        if row_index + 1 > 8:
            return
        elif self._active_player in square_occupant or "NONE" in square_occupant:
            return
        elif self._active_player not in self._game_board[row_index+1][col_index]:
            if "NONE" not in self._game_board[row_index + 1][col_index]:
                return

        captured_piece = self._game_board[row_index][col_index]
        self._num_captured_pieces[captured_piece] += 1
        self._game_board[row_index][col_index] = "NONE"

    def capture_pieces_left(self, row_index, col_index):
        """
        Takes two parameters - the row index and the column index of a square, and checks
        for captures that exist to the left of the given square. If there is a capture, then the
        method will remove the captured pieces and update the number captured for the color of
        the pieces captured.
        """
        if col_index < 0:
            return
        elif col_index - 1 >= 0:
            if "NONE" in self._game_board[row_index][col_index - 1]:
                return

        square_occupant = self._game_board[row_index][col_index]

        #  CHECK FOR CORNER CAPTURES
        if row_index == 0 and col_index == 0:
            bottom_occupant = self._game_board[row_index + 1][col_index]
            if self._active_player in bottom_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1
        elif row_index == 8 and col_index == 0:
            top_occupant = self._game_board[row_index - 1][col_index]
            if self._active_player in top_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1

        if self._active_player in square_occupant:
            return
        elif "NONE" in square_occupant:
            return

        self.capture_pieces_left(row_index, col_index - 1)  # recursive call

        if col_index - 1 < 0:
            return
        elif self._active_player in square_occupant or "NONE" in square_occupant:
            return
        elif self._active_player not in self._game_board[row_index][col_index-1]:
            if "NONE" not in self._game_board[row_index][col_index - 1]:
                return

        captured_piece = self._game_board[row_index][col_index]
        self._num_captured_pieces[captured_piece] += 1
        self._game_board[row_index][col_index] = "NONE"

    def capture_pieces_right(self, row_index, col_index):
        """
        Takes two parameters - the row index and the column index of a square, and checks
        for captures that exist to the right of the given square. If there is a capture, then the
        method will remove the captured pieces and update the number captured for the color of
        the pieces captured.
        """
        if col_index > 8:
            return
        elif col_index + 1 <= 8:
            if "NONE" in self._game_board[row_index][col_index+1]:
                return

        square_occupant = self._game_board[row_index][col_index]

        # CHECK CORNER CAPTURES
        if row_index == 0 and col_index == 8:
            bottom_occupant = self._game_board[row_index + 1][col_index]
            if self._active_player in bottom_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1
        elif row_index == 8 and col_index == 8:
            top_occupant = self._game_board[row_index - 1][col_index]
            if self._active_player in top_occupant:
                self._game_board[row_index][col_index] = "NONE"
                self._num_captured_pieces[square_occupant] += 1

        if self._active_player in square_occupant:
            return
        elif "NONE" in square_occupant:
            return

        self.capture_pieces_right(row_index, col_index + 1)  # recursive call

        if col_index + 1 > 8:
            return
        elif self._active_player in square_occupant or "NONE" in square_occupant:
            return
        elif self._active_player not in self._game_board[row_index][col_index+1]:
            if "NONE" not in self._game_board[row_index][col_index + 1]:
                return

        captured_piece = self._game_board[row_index][col_index]
        self._num_captured_pieces[captured_piece] += 1
        self._game_board[row_index][col_index] = "NONE"

    def capture_pieces(self, row_index, col_index):
        """
        Takes two parameters – the row index and the column index of a square. It checks for valid captures,
        removes captured pieces from the _game_board, increments the _num_of_captured pieces for the color
        of the captured pieces, and changes the game_state when appropriate. This method will be used by
        the make_move method to make captures after a valid move is made.
        """
        # CAPTURE ABOVE
        if row_index - 1 >= 0:
            top_occupant = self._game_board[row_index - 1][col_index]
            if self._active_player not in top_occupant and "NONE" not in top_occupant:
                self.capture_pieces_above(row_index - 1, col_index)
        # CAPTURE BELOW
        if row_index + 1 <= 8:
            bottom_occupant = self._game_board[row_index + 1][col_index]
            if self._active_player not in bottom_occupant and "NONE" not in bottom_occupant:
                self.capture_pieces_below(row_index + 1, col_index)
        # CAPTURE LEFT
        if col_index - 1 >= 0:
            left_occupant = self._game_board[row_index][col_index - 1]
            if self._active_player not in left_occupant and "NONE" not in left_occupant:
                self.capture_pieces_left(row_index, col_index - 1)
        # CAPTURE RIGHT
        if col_index + 1 <= 8:
            right_occupant = self._game_board[row_index][col_index + 1]
            if self._active_player not in right_occupant and "NONE" not in right_occupant:
                self.capture_pieces_right(row_index, col_index + 1)

    def make_move(self, from_location, to_location):
        """
        Takes two parameters - strings that represent the square moved from and the square moved to (in
        algebraic notion). If the square being moved from does not contain a piece belonging to the
        player whose turn it is, or if the indicated move is not legal, or if the game has already been
        won, then it returns False. Otherwise, it makes the indicated move, remove any captured pieces,
        update the game state if necessary, update whose turn it is, and return True.
        """
        from_square_row_index = self.convert_algebraic_notation(from_location)[0]
        from_square_col_index = self.convert_algebraic_notation(from_location)[1]

        to_square_row_index = self.convert_algebraic_notation(to_location)[0]
        to_square_col_index = self.convert_algebraic_notation(to_location)[1]

        validation_result = self.validate_move(from_location, to_location)  # validate move & continue if valid

        if validation_result:
            self._game_board[to_square_row_index][to_square_col_index] = self.get_square_occupant(from_location)
            self._game_board[from_square_row_index][from_square_col_index] = "NONE"

            self.capture_pieces(to_square_row_index, to_square_col_index)  # CAPTURE PIECES

            if self._num_captured_pieces["BLACK"] >= 8:
                self._game_state = "RED_WON"
            elif self._num_captured_pieces["RED"] >= 8:
                self._game_state = "BLACK_WON"

            if "BLACK" in self._active_player:
                self._active_player = "RED"
            elif "RED" in self._active_player:
                self._active_player = "BLACK"

            return True

        return False

    def get_square_occupant(self, location):
        """
        Takes one parameter, a string in algebraic notation representing a square location (such as 'i7'),
        and returns 'RED', 'BLACK', or 'NONE', depending on whether the specified square is occupied
        by a red piece, a black piece, or neither. This method will be used by the make_move method
        n validating moves from and to squares.
        """
        square_row_index = self.convert_algebraic_notation(location)[0]
        square_col_index = self.convert_algebraic_notation(location)[1]

        return self._game_board[square_row_index][square_col_index]
