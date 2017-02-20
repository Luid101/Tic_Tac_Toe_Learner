class TicTacToeController:
    """
    Controller for the Tic Tac Toe game.
    :ivar _board[char]: An array representation of the board
    :ivar _done: A boolean that represents the game's state
    :ivar _player_order[Player]: Tic tac toe players in order of who goes first
    :ivar _turns: An integer representing the number of turns
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
        self._player1 = player1
        self._player2 = player2
        self._player_order = [self._player1, self._player2]  # Arranged in order
        # of who goes first.
        self._done = False
        self._turns = 0

    def get_board(self):
        """
        :return: Game board
        """
        return self._board

    def get_current_player(self):
        """
        :return: The current player
        """
        return self._player_order[self._turns % 2]

    def get_is_done(self):
        """
        :return: True if the game is done, False otherwise
        """
        return self._done

    def get_player1(self):
        """
        :return: Player 1
        """
        return self._player1

    def get_player2(self):
        """
        :return: Player 2
        """
        return self._player2

    def get_players(self):
        """
        :return: Array of players
        """
        return self._player_order

    def get_turns(self):
        """
        :return: Number of turns
        """
        return self._turns

    def get_winner(self):
        """
        :return: The winner of the game
        """
        return self._player_order[(self._turns - 1) % 2]  # Number of turns gets
        # incremented before checking the winner

    def convert_board(self, board):
        """
        Converts the board into a format that can be processed by the AI. 0 for
        empty space, 1 for player's moves, 2 for AI's moves.
        :param board: an array of characters
        :return: an array of integers
        """
        ai_board = []
        for symbol in board:
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
        print("5")
        player_turn = self._turns % 2  # Determines who plays this turn
        if not self._done:
            print("2")
            if self._player_order[player_turn].get_mode() == 0:  # Human
                print("human")
                # x if first one to go, o if second one to go
                if self._board[index] == '-':
                    print("replace")
                    # Replace with x/o if there's an empty spot at board[index]
                    self._board[index] = 'x' if player_turn == 0 else 'o'
                    self._turns += 1

            elif self._player_order[player_turn].get_mode() == 1:  # AI
                print("ai")
                # x if first one to go, o if second one to go
                ai_move = self._player_order[player_turn].get_ai_move(
                    self.convert_board(self._board))  # Gets the AI's next move
                # by sending the current board configuration
                if self._board[ai_move] == '-':
                    # Replace with x/o if an empty spot exists at board[ai_move]
                    self._board[ai_move] = 'x' if player_turn == 0 else 'o'
                    self._turns += 1

    def reset(self):
        """
        Resets game
        :return: None
        """
        if self._done:
            self._done = False
            self._turns = 0
            self._player_order[0], self._player_order[1] = \
                self._player_order[1], self._player_order[0]  # Switch the order
            # of the two players
            self._board = ['-' for symbol in self._board]

    def tie(self):
        """
        Determines if the game is a tie or not
        :return: True if the game is a tie, False otherwise
        """
        draw = '-' not in self._board and self._turns > 8
        if draw:
            self._done = True
            for player in self._player_order:
                player.draw()
        return draw

    def win(self):
        """
        Finds a winning row, column, or diagonal
        :return: True if there's a winner, False otherwise
        """
        winner = False
        win_positions = [[self._board[0], self._board[1], self._board[2]],
            [self._board[3], self._board[4], self._board[5]],
            [self._board[6], self._board[7], self._board[8]],
            [self._board[0], self._board[3], self._board[6]],
            [self._board[1], self._board[4], self._board[7]],
            [self._board[2], self._board[5], self._board[8]],
            [self._board[0], self._board[4], self._board[8]],
            [self._board[2], self._board[4], self._board[6]]]

        for symbol in ['x', 'o']:
            for position in win_positions:
                if all(x == symbol for x in position):
                    winner = True
                    break

        if winner:
            # A player won
            self._done = True
            if self._turns % 2 == 1:
                # Turns get incremented before checking for the winner, so if
                # the turn is an odd number, then the first player won
                self._player_order[0].won()
                self._player_order[1].lost()
            else:
                # Second player won
                self._player_order[1].won()
                self._player_order[0].lost()

        return winner


class Player:
    """
    A tic tac toe player
    :ivar _ai: AI engine if _mode == 1
    :ivar _mode: 0 for human, 1 for AI
    :ivar _name: Name
    :ivar _num: Player number, nothing to do with order
    :ivar _score: Player score
    """
    def __init__(self, mode, num, name, ai=None):
        """
        :param mode: 0 for human, 1 for AI
        :param num: Player number
        :param name: Name
        :param ai: AI Engine if _mode == 1
        :return: None
        """
        self._mode = mode
        self._name = name
        self._num = num
        self._score = 0
        self._ai = ai if self._mode == 1 else None

    def get_ai_move(self, board):
        """
        :param board: Tic tac toe board
        :return: Integer where the AI wants to make a move
        """
        return self._ai.move(board) if self._mode == 1 else None

    def get_mode(self):
        """
        :return: 0 if the player is human, 1 if the player is AI
        """
        return self._mode

    def get_name(self):
        """
        :return: Player name
        """
        return self._name

    def get_num(self):
        """
        :return: The player's number
        """
        return self._num

    def get_score(self):
        """
        :return: The player's score
        """
        return self._score

    def draw(self):
        """
        If the player is an AI, it runs the AI learning algorithm and returns a
        message. (To be implemented)
        :return: A message from the AI
        """
        pass

    def lost(self):
        """
        If the player is an AI, it runs the AI learning algorithm and returns a
        message.
        :return: A message from the AI
        """
        return self._ai.has_lost() if self._mode == 1 else None

    def won(self):
        """
        Increments the player's score by 1. If the player is an AI, it runs the
        AI learning algorithm and returns a message.
        :return: A message from the AI
        """
        self._score += 1
        return self._ai.has_won() if self._mode == 1 else None
