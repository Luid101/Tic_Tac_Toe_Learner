class TicTacToeController:
    """
    Controller for the Tic Tac Toe game.

    :ivar _board[char]: An array representation of the board
    :ivar _done: A boolean that represents the game's state
    :ivar _player_order[Player]: Tic tac toe players in order of who goes first
    :ivar _turns: An integer representing the number of turns
    :ivar _symbols: Array of valid symbols
    """
    def __init__(self, player1, player2):
        """
        :param player1: A player object
        :param player2: A player object
        :return: None
        """
        self._board = ['-', '-', '-',
                       '-', '-', '-',
                       '-', '-', '-']
        self._player_order = [player1, player2]  # Arranged in order of who goes
        # first.
        self._done = False
        self._turns = 0

    def convert_board(self, board):
        """
        Converts the board into a format that can be processed by the AI. 0 for
        empty space, 1 for player's moves, 2 for AI's moves.

        :param board: an array of characters
        :return: an array of integers
        """
        ai_board = []
        for symbol in self._board:
            if symbol == 'x':
                # First one to go
                ai_board.append(self._player_order[0].get_num())
            elif symbol == 'o':
                # Second one to go
                ai_board.append(self._player_order[1].get_num())
            else:
                # Empty spot
                ai_board.append(0)
        return ai_board

    def move(self, index):
        """
        Makes a move at an index if the player is human
        :param index: Position on the board where to make a move
        :return: None
        """
        player_turn = self._turns % 2  # Determines who plays this turn

        if self._player_order[player_turn].get_mode == 0: # Human
            # x if first one to go, o if second one to go
            if self._board[index] == '-':
                # Replace with x/o if there's an empty spot at board[index]
                self._board[index] = 'x' if player_turn == 0 else 'o'
                self._turns += 1

        elif self._player_order[player_turn].get_mode == 1: # AI
            # x if first one to go, o if second one to go
            ai_move = self._player_order[player_turn]
            if self._board[ai_move] == '-':
                # Replace with x/o if there's an empty spot at board[ai_move]
                self._board[ai_move] = 'x' if player_turn == 0 else 'o'
                self._turns += 1

    def win(self):
        """
        Finds a winning row, column, or diagonal
        :return:
        """
        return self._board[0] == self._board[1] == self._board[2] or \
               self._board[3] == self._board[4] == self._board[5] or \
               self._board[6] == self._board[7] == self._board[8] or \
               self._board[0] == self._board[3] == self._board[6] or \
               self._board[1] == self._board[4] == self._board[7] or \
               self._board[2] == self._board[5] == self._board[8] or \
               self._board[0] == self._board[4] == self._board[8] or \
               self._board[2] == self._board[4] == self._board[6]


class Player:
    """
    A tic tac toe player
    """
    def __init__(self, mode, num, ai=None):
        self._mode = mode
        self._num = num
        self._score = 0
        self._ai = None
        if self._mode == 1:
            self._ai = ai

    def get_ai_move(self, board):
        """
        :param board: Tic tac toe board
        :return: Integer where the AI wants to make a move
        """
        if self._mode == 1:
            return self._ai.move(board)

    def get_mode(self):
        """
        :return: 0 if the player is human, 1 if the player is AI
        """
        return self._mode

    def get_num(self):
        """
        :return: The player's number
        """
        return self._num









