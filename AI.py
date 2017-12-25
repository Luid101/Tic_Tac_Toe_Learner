import random
import os.path
from functions import *

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
        self.game_boards_current = []
        self.game_boards_memory = dict()    
        self.file_name = "memory.txt"

        # Certainty + randomness must be >= 1

        # a level of how random the ai behaves
        # 0 => not random at all
        self.randomness = 1

        # a level of how certain the ai behaves
        # 0 => not certain at all
        self.certainty = 10

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
        '''
        # figure out the best move
        print("Next moves:")
        for x in next_moves_list:
            print(x)
        '''
        
        # create list of [[index of board move, new board], value of move]
        index_value_lst = [[x, self.get_board_value(x[1])] for x in next_moves_list]
        '''
        print("\nBoard moves with values:")
        for x in index_value_lst:
            print(x)
        '''

        # create a new list of just the weights of those moves
        weights_list = [x[1] for x in index_value_lst]

        # apply a 'positizer' to the list of weights 
        weights_list = positize_values(weights_list)
        '''
        print("\nPositizer representation:")
        for x in weights_list:
            print(x)
        '''

        # apply the softmax function
        weights_list = softmax(weights_list)
        '''
        print("\nSoftmax representation:")
        for x in weights_list:
            print(x)
        '''

        # randomly pick an index
        chosen_index = weighted_choice(weights_list)

        # get data from choice index
        choice_data = index_value_lst[chosen_index]

        '''
        # print data of index_value_lst
        print("chosen index:{}, \nchosen data:{}, \nretunred data:{}\n\n".format(\
                    chosen_index, choice_data, choice_data[0][0]))
        '''

        # get a random index
        index = random.randint(0, len(next_moves_list)-1)
        best_move = next_moves_list[index]

        for next_move in next_moves_list:
            # if the next move is better, it replaces the best move
            if self.get_board_value(best_move[1]) < self.get_board_value(next_move[1]):
                best_move = next_move
        
        # factor in how much randomness the ai has
        randomness = self.randomness
        picks = []
        while randomness != 0:
            picks.append(0)
            randomness -= 1
        # factor in how certain the ai is
        centanty = self.certainty
        while centanty != 0:
            picks.append(1)
            centanty -= 1
        
        # decide if or not to use the weighted choice
        decision = random.choice(picks)
        
        if decision == 1:
            # don't use the weighted choice
            self.game_boards_current.append(best_move[1])
            print("chose certainly")
            return best_move[0]
        
        '''
        print("chose randomly")
        '''

        # add the next move that we are going to make to a list of all boards seen so far
        # the game_boards current.
        self.game_boards_current.append(choice_data[1])

        # return the index of where to play the next move
        return choice_data[0][0]

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
            value = 0

        return value

    def has_lost(self):
        return self.remember_boards(-100)

    def has_drawn(self):
        return self.remember_boards(1)

    def has_won(self):
        return self.remember_boards(100)

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
                self.game_boards_memory[temp_list[0]] = int(temp_list[1])
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


    




