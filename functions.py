"""
This file contains all the status functions used by AI.py
"""

import random

def positize_values(values):
    """
    Given a list of values, move them all to 
    the positive range. keeping the original
    relationship between them.

    :param values: lst[]
    :return: lst[]
    """

    min_val = min(values)
    if min_val < 0:
        new_vals = []
        for value in values:
            new_vals.append(value + abs(min_val))
        return new_vals
    else:
        return values

def convert_to_list(dictionary):
    """
    Takes a dictionary and converts it to 
    a 2d list with key in index 0 and value
    in index 1.

    :param dictionary: any dictionary
    :return: lst[lst[]]
    """

    lst = []
    for key in dictionary:
        lst.append([key, dictionary[key]])

    return lst 

def softmax(weights):
    """
    Given a list of weights, makes sum of all 
    the weights equal 1. Using the softmax function.

    :param weights: lst[]
    :return: lst[]
    """
    total = sum(weights)
    if total == 0: 
        return [1/len(weights) for x in weights]
    return [x/total for x in weights]

def weighted_choice(weights):
    """
    Given a list of weights, it returns an index randomly, 
    according to these weights.
    
    Credit: https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
    Author: (probably)Eli Bendersky

    >>> weighted_choice([2, 3, 5])
    *returns 0 with a probaility of .2*

    :param weights: lst[]
    :return: int
    """
    total = 0
    winner = 0
    for i, w in enumerate(weights):
        total += w
        if random.random() * total < w:
            winner = i
    return winner

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