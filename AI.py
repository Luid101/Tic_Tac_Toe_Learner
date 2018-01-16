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
        :return:
        """
        self.self_save = True
        self.is_learning = True
        self.game_boards_current = []
        self.game_boards_memory = dict()    
        self.file_name = "memory.txt"
        self.previous_state = None
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
        >>> board = [0, 0, 0, 0, 1, 0, 0, 0, 0]
        >>> index = ai.move(board)
        >>> print(index)
        0
        >>> len(ai.game_boards_current)
        1
        >>> board_better = [0, 2, 0, 0, 1, 0, 0, 0, 0]
        >>> board_better_key = str(board_better)
        >>> ai.game_boards_memory[board_better_key] = 5
        >>> index = ai.move(board)
        >>> print(index)
        1
        """

        # generate all possible next moves
        next_moves_list = generate_next(board)

        # figure out the best move
        # get a random index
        index = random.randint(0, len(next_moves_list)-1)
        best_move = next_moves_list[index]

        for next_move in next_moves_list:
            # if the next move is better, it replaces the best move
            if self.get_board_value(best_move[1]) < self.get_board_value(next_move[1]):
                best_move = next_move

        # add the next move that we are going to make to a list of all boards seen so far
        # the game_boards current.
        self.game_boards_current.append(best_move[1])
        self.backtrack(self.get_board_value(best_move[1]))
        self.previous_state = best_move[1]
        # return the index of where to play the next move
        return best_move[0]

    def backtrack(self,current_move_value):
        if self.is_learning:
            if self.previous_state != None:
                self.game_boards_memory[str(self.previous_state)] +=  0.99*(current_move_value-self.game_boards_memory[str(self.previous_state)])
                
            if self.self_save:
                print("here: {}".format(self.self_save))
                self.save()
            else:
                print("No save")
                
    def get_board_value(self, board):
        """
        returns the value of that board in the computers memory.

        board:  a list of 9 spaces that signals a game board.
        :param board: list[]
        :return: int

        >>> ai = AI()
        >>> board = [0,0,0]
        >>> board_key = str(board)
        >>> ai.get_board_value(board_key)
        0
        >>> ai.game_boards_memory[board_key] = 5
        >>> ai.get_board_value(board_key)
        5
        """
        # use string representation as the key of the dictionary
        board_key = str(board)
        if board_key in self.game_boards_memory:
            value = self.game_boards_memory.get(board_key)
        else:
            value = 0.5
            self.game_boards_memory[board_key] = value

        return value

    def has_lost(self):
        self.backtrack(0)
        self.previous_state = None
        ##return self.remember_boards(-1)

    def has_drawn(self):
        self.backtrack(0.5)
        self.previous_state = None
        #return self.remember_boards(-0.5)

    def has_won(self):
        self.backtrack(1)
        self.previous_state = None
        ##return self.remember_boards(1)
    
    def stop_learning(self):
        self.is_learning = False
        print("Stopped learning")
        
    def start_learning(self):
        self.is_learning = True
        print("Started learning")
    
    def stop_self_saving(self):
        self.self_save = False
        print("Stopped self saving")
        
    def start_self_saving(self):
        self.self_save = True
        print("Started self saving")

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
        >>> board = [0,1,0,0]
        >>> 0 <= ai.move(board) <= len(board)
        True
        >>> board2 = [0,0,1,0]
        >>> 0 <= ai.move(board2) <= len(board2)
        True
        >>> print(ai.has_won())
        Learned 2 new boards, And changed how I look at 0 boards
        <BLANKLINE>
        >>> s = 0
        >>> for board in ai.game_boards_memory: s += ai.game_boards_memory[board]
        >>> s
        1
        >>> board3 = [1,0,0,0]
        >>> 0 <= ai.move(board3) <= len(board3)
        True
        >>> board4 = [1,2,0,0]
        >>> board4_lost = ai.move(board4)
        >>> print(ai.has_lost())
        Learned 2 new boards, And changed how I look at 0 boards
        <BLANKLINE>
        >>> new_board = ai.move(board4)
        >>> str(new_board) == str(board4_lost)
        False
        """
        # info data about what the computer is learning
        changed = 0
        added = 0

        for board in self.game_boards_current:
            value = multiplier * self.game_boards_current.index(board)

            # check if that item is in the dictionary.
            # if it is, add value to it,
            # if not, create a new key with the board and make it point to value.
            board_key = str(board)
            if board_key in self.game_boards_memory:
                self.game_boards_memory[board_key] += value
                changed += 1
            else:
                self.game_boards_memory[board_key] = value
                added += 1

        # after the loop,
        # now clear out the list of boards for the current game
        self.game_boards_current = []
        s = "Moves learned: " + str(added) + ", Moves modified: " + str(changed)

        # save stuff that is remembered into a my
        self.save()
        return s

    def save(self):
        """
        Save the contents of the database into a file.

        :param file_name: str
        :return: number of entries saved
        """
        
        print("Saving")
        
        file_name = self.file_name
        entries = 0
        target_file = open(file_name, 'w')

        for key in self.game_boards_memory:
            target_file.write(str(key) + ":" + str(self.game_boards_memory[key]) + "\n")
            entries += 1

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
            temp_list = line.strip("\n").split(":")
            if len(temp_list) == 2:
                self.game_boards_memory[temp_list[0]] = float(temp_list[1])
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




