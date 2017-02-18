from Board import *




board = Board()

if __name__ == '__main__':
    while not board.has_won():
        board.user_turn()




