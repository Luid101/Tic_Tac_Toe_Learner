import random
import os.path

class AI:
    def __init__(self):
        """
        This initialises a new ai with a:
        1) game_boards list to store
            all the games played so far.
        2) the ai's internal memory that
            stores all boards its seen
            in a dictionary.

        * bugs:
            1) have it account for losses
            2) have it be able to play itself
            3)
        :return:
        """
        self.game_boards_current = []
        self.game_boards_memory = dict()    # have this initialize from a file soon
        self.file_name = "memory.txt"

        # check if the file exists
        if os.path.isfile(self.file_name):
            self.load()

    def move(self, board):
        """
        Takes in a board and returns what index of
            board to play the next move.
        board:  a list of 9 spaces that signals a game board.
        :param board: list[]
        :return: int

        >>> ai = AI()
        >>> prev_board = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        >>> index = ai.move(prev_board)
        >>> next_board = prev_board[:]
        >>> next_board[index] = 2
        >>> len(ai.game_boards_current)
        1
        >>> board_better = [0, 2, 0, 0, 1, 0, 0, 0, 0]
        >>> board_better_key = str(board_better)
        >>> ai.game_boards_memory[str(prev_board)] = dict()
        >>> ai.game_boards_memory[str(prev_board)][str(next_board)] = 5
        >>> index2 = ai.move(prev_board)
        >>> index2 == index
        True
        """
        # set previous board
        prev_board = board

        # generate all possible next moves
        next_moves_list = generate_next(board)

        # figure out the best move
        # get a random index
        index = random.randint(0, len(next_moves_list)-1)
        best_move = next_moves_list[index]

        for next_move in next_moves_list:
            # if the next move is better, it replaces the best move
            if self.get_board_value(prev_board, best_move[1]) < self.get_board_value(prev_board, next_move[1]):
                best_move = next_move

        # add the next move that we are going to make to a list of all boards seen so far
        # the game_boards current.
        self.game_boards_current.append([prev_board, best_move[1]])

        # return the index of where to play the next move
        return best_move[0]

    def get_board_value(self, prev_board, next_board):
        """
        returns the value of that board (in-relation to the previous board) in the computers memory.

        prev_board:  a list of 9 spaces that signals a game board.
        next_board:  a list of 9 spaces that signals a game board.
        :param prev_board: list[]
        :param next_board: list[]
        :return: int

        >>> ai = AI()
        >>> prev_board = [0,0,0]
        >>> next_board = [0,0,1]
        >>> prev_board_key = str(prev_board)
        >>> next_board_key = str(next_board)
        >>> ai.get_board_value(prev_board_key,next_board_key)
        0
        >>> ai.game_boards_memory[prev_board_key]= dict()
        >>> ai.game_boards_memory[prev_board_key][next_board_key] = 5
        >>> ai.get_board_value(prev_board_key,next_board_key)
        5
        """
        # use string representation as the key of the dictionary
        # access the next board's value from inside the index of the previous board
        prev_board_key = str(prev_board)
        next_board_key = str(next_board)
        if prev_board_key in self.game_boards_memory:
            if next_board_key in self.game_boards_memory[prev_board_key]:
                value = self.game_boards_memory[prev_board_key][next_board_key]
            else:
                value = 0
        else:
            value = 0

        return value

    def has_lost(self):
        return self.remember_boards(-2)

    def has_drawn(self):
        return self.remember_boards(1)

    def has_won(self):
        return self.remember_boards(2)

    def remember_boards(self, multiplier):
        """
        Takes all the boards in boards current,
            multiplies their index by multiplier to get new_value,
            and if board already exists, it add's value to the value under that board key,
            if not, then it creates a new key that points to value.
        :param multiplier:
        :return: [number of entries added, number of entries changed]

        test that this code works
        >>> ai = AI()
        >>> prev_board = [0,1,0,0]
        >>> index = ai.move(prev_board)
        >>> next_board = prev_board[:]
        >>> next_board[index] = 2
        >>> index2 = ai.move(next_board)
        >>> next_board2 = next_board[:]
        >>> ai.has_lost()
        'Moves learned: 2, Moves modified: 0'
        >>> next_index = ai.move(next_board)
        >>> index2 != next_index
        True
        >>> print ai.game_boards_memory
        {'[0, 1, 0, 0]': {'[2, 1, 0, 0]': -2}, '[2, 1, 0, 0]': {'[2, 1, 2, 0]': -4}}
        """
        # info data about what the computer is learning
        changed = 0
        added = 0

        for boards in self.game_boards_current:
            value = multiplier * (self.game_boards_current.index(boards) + 1)

            # check if that item is in the dictionary.
            # if it is, , add value to it,
            # if not, create a new key with the board and make it point to value.
            prev_board_key = str(boards[0])
            next_board_key = str(boards[1])

            # check if prev_board_key exists in memory
            if prev_board_key in self.game_boards_memory:
                # check if the value of next_board is in the dictionary
                if next_board_key in self.game_boards_memory[prev_board_key]:
                    self.game_boards_memory[prev_board_key][next_board_key] += value
                    changed += 1
                # if the value of next_board_key is not in the dictionary, then add it in.
                else:
                    self.game_boards_memory[prev_board_key][next_board_key] = value
                    added += 1
            # if prev_board_key deos not exist in memory, then create it and attach a new connection to next_board_key
            else:
                self.game_boards_memory[prev_board_key] = dict()
                self.game_boards_memory[prev_board_key][next_board_key] = value
                added += 1

        # after the loop,
        # now clear out the list of boards for the current game
        self.game_boards_current = []
        s = "Moves learned: " + str(added) + ", Moves modified: " + str(changed)

        # save stuff that is remembered into a my memory

        self.save()

        return s

    def save(self):
        """
        Save the contents of the database into a file.

        :param file_name: str
        :return: number of entries saved
        """
        file_name = self.file_name
        entries = 0
        target_file = open(file_name, 'w')

        for key in self.game_boards_memory:
            target_file.write(str(key) + ":")
            for next_board_key in self.game_boards_memory[key]:
                target_file.write(str(next_board_key) + "%" + str(self.game_boards_memory[key][next_board_key]) + ";")
            target_file.write("\n")
            # entries += 1

        target_file.close()

    def load(self):
        """
        Load the contents of a file into its database (dict)

        :param file_name: str
        :return: number of entries loaded
        """
        file_name = self.file_name
        entries = 0

        target_file = open(file_name, 'r')

        for line in target_file:
            temp_list = line.strip("\n").strip(";").split(":")
            if len(temp_list) == 2:
                self.game_boards_memory[temp_list[0]] = dict()
                next_list = temp_list[1].split(";")
                for element in next_list:
                    element_list = element.split("%")
                    self.game_boards_memory[temp_list[0]][element_list[0]] = int(element_list[1])
                    entries += 1

        return entries

    def get_memory(self):
        """
        Return a string representation of the ai's memory
        :return:
        """
        s = ""
        for board_key in self.game_boards_memory:
            s += (str(board_key) + "\n" + str(self.game_boards_memory[board_key]) + "\n")
        return s

def generate_next(board):
    """
    Takes a board and returns a list of
        all possible moves that can be made by the ai on that board.
        It also includes the move needed to get to that board.

    board:  a list of 9 spaces that signals a game board.

    :param board: list[]
    :return: list[list[int, board]]

    # test out code
    >>> board = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    >>> next_moves_list = generate_next(board)
    >>> for board in next_moves_list: print(str(board[0]) + "\\n" + show_board(board[1]))
    0
    200
    010
    000
    <BLANKLINE>
    1
    020
    010
    000
    <BLANKLINE>
    2
    002
    010
    000
    <BLANKLINE>
    3
    000
    210
    000
    <BLANKLINE>
    5
    000
    012
    000
    <BLANKLINE>
    6
    000
    010
    200
    <BLANKLINE>
    7
    000
    010
    020
    <BLANKLINE>
    8
    000
    010
    002
    <BLANKLINE>
    """
    # store next moves here
    next_moves_list = []

    # loop through all possible moves
    for i in range(len(board)):
        if board[i] == 0:
            # generate new board and add it to next_moves_list.
            new_board = board[:]
            new_board[i] = 2        # the ai's symbol is represented by a 2
            next_moves_list.append([i, new_board])

    return next_moves_list


def show_board(board):
    """
    Takes a board and prints out it's status.

    :param board: a list of length 9 that signifies a game board
    :return: null

    # test out the code.
    >>> board = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    >>> show_board(board)
    000
    010
    000
    """
    s = ""
    # loop through the board
    for i in range(9):
        s += str(board[i])
        if (((i+1) % 3) == 0) and (i != 0):
            s += "\n"
    return s

# if __name__ == "__main__":
#     # test out save
#     # ai = AI()
#     # ai.load()
#     #
#     # board1 = [0, 0, 0, 0, 1, 2, 0, 0, 0]
#     # ai.move(board1)
#     #
#     # board1 = [0, 2, 0, 0, 1, 0, 0, 0, 0]
#     # ai.move(board1)
#     #
#     # board1 = [0, 2, 0, 0, 1, 0, 0, 0, 0]
#     # ai.move(board1)
#     #
#     # board1 = [0, 2, 0, 0, 1, 1, 1, 0, 0]
#     # ai.move(board1)
#     # ai.has_won()
#     # ai.save()
#     #
#     # print(ai.game_boards_memory)




