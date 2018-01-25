"""
This file contains all the status functions used by AI.py
"""
import random

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