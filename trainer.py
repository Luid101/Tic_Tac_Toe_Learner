from AI import *
import random
import time
import sys

# constants
TIMECONST = 's'
NUMCONST = 'n'


def train_for(duration):
    """
    Train the ai for a given amount of time
    :param duration:
    :return:
    """
    start_time = int(time.time())
    end_time = int(time.time())

    trainer_wins = 0
    ai_wins = 0
    draws = 0

    while end_time <= (start_time + duration):
        # get some stats
        stats = train(1)
        trainer_wins += stats[0]
        ai_wins += stats[1]
        draws += stats[2]

        # check end time
        end_time = int(time.time())

    # print out stats
    print("Score[ Trainer : " + str(trainer_wins) + ", AI : " + str(ai_wins) + ", Draws: " + str(draws) + " ]\n")


def train(num, vs_ai=True):
    """
    Train the ai num times, using the default ai trainer.
    Or using the ai itself if needed.

    :param num: int
    :param vs_ai: boolean
    :return: lst[]
    """

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn = True
    ai = AI()
    past_turn = turn

    # get other ai if needed
    ai_trainer = None
    if vs_ai:
        ai_trainer = AI()

    # get some stats
    trainer_wins = 0
    ai_wins = 0
    draws = 0

    # for times given
    for times in range(num):
        turn = past_turn

        # while the game is not over
        while game_over(board) == -1:
            # if it is the trainers turn
            if turn:
                # get move from other ai or trainer
                index = 0
                if vs_ai:
                    reflected_board = reflect_board(board)
                    index = ai_trainer.move(reflected_board)
                    print("Trainer AI played in :", index)
                else:
                    index = get_trainer_move(board)
                    print("Trainer played in :", index)
                
                board[index] = 1
                turn = not turn
                
                print(show_board(board))

            # if it is the ai's turn
            else:
                index = ai.move(board)
                board[index] = 2
                turn = not turn
                print("AI played in :", index)
                print(show_board(board))

        # figure out who won
        if game_over(board) == 1:
            print("Trainer won!")
            ai.has_lost()
            trainer_wins += 1

            # notify the ai trainer if needed
            if vs_ai:
                ai_trainer.has_won()

        elif game_over(board) == 2:
            print("AI won!")
            ai.has_won()
            ai_wins += 1

            # notify the ai trainer if needed
            if vs_ai:
                ai_trainer.has_lost()

        elif game_over(board) == 0:
            print("it was a draw!")
            ai.has_drawn()
            draws += 1

            # notify the ai trainer if needed
            if vs_ai:
                ai_trainer.has_drawn()

        # print out stats
        print("Score[ Trainer : " + str(trainer_wins) + ", AI : " + str(ai_wins) + ", Draws: " + str(draws) + " ]\n")

        # reset the board
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        past_turn = not past_turn

    return [trainer_wins, ai_wins, draws]

def reflect_board(board):
    """
    Given a board with 1's and 2's
    make all the 1's into 2's and 2's
    into ones.

    :board: lst[]
    :return: lst[]
    """
    
    new_board = []
    for number in board:
        if number == 1:
            new_board.append(2)
        elif number == 2:
            new_board.append(1)
        else:
            new_board.append(0)

    return new_board

def get_trainer_move(board, error=5):
    """
    get move from trainer.
    the trainer see's itself as 1.

    :param board:
    :return:
    """

    # check if it can win
    assessments = check_moves(board)
    next_move = -1

    if len(assessments) > 0:
        # print(assessments)
        for move in assessments:
            # if move results in trainer winning, then make it
            if move[0] == 1:
                return move[2]

            # if move results ai winning, then make a counter it
            if move[1] == 2:
                next_move = move[2]

    # make the trainer make mistakes 1 out of error(default 5 times)
    mistake = random.randint(1, error)

    if next_move != -1 and mistake != 1:
        return next_move

    # loop through the board and make a random selection from all the possible moves
    possible_moves = []
    for index in range(len(board)):
        if board[index] == 0:
            possible_moves.append(index)

    next_move = random.choice(possible_moves)

    return next_move


def check_moves(board):
    """
    gets the outcome of each move using that board.
    the trainer see's itself as 1.
    :param board:
    :return: [int, int]
    """
    result = []

    # loop through the entire board
    for index in range(len(board)):
        if board[index] == 0:
            board2 = board[:]

            # check if I can win
            board2[index] = 1
            outcome_p1 = game_over(board2)

            # check if the opponent can win
            board2[index] = 2
            outcome_p2 = game_over(board2)

            result.append([outcome_p1, outcome_p2, index])

    return result


def game_over(board):
    """
    returns 1 or 2 or 0 if there is a winner and -1 if the game is still going on.
    1: the winner is the trainer
    2: the winner is the ai
    0: there is a draw
    -1: the game is still going on
    :param board: list[]
    :return: int
    """

    # check for horizontal wins
    if board[0] == board[1] == board[2] != 0:
        return board[0]
    elif board[3] == board[4] == board[5] != 0:
        return board[3]
    elif board[6] == board[7] == board[8] != 0:
        return board[6]

    # check verticals
    elif board[0] == board[3] == board[6] != 0:
        return board[0]
    elif board[1] == board[4] == board[7] != 0:
        return board[1]
    elif board[2] == board[5] == board[8] != 0:
        return board[2]

    # check diagonals
    elif board[0] == board[4] == board[8] != 0:
        return board[0]
    elif board[2] == board[4] == board[6] != 0:
        return board[2]

    # check for draw
    elif 0 not in board:
        return 0

    # if none of this happens, then the game is still going on
    return -1

def main(sys):
    """
    Get data from arguments and use trainer.

    Usage:
    pythonX trainer.py [ s | n ] [ time_in_seconds | num_in_iterations ]

    Example:

    $> python trainer.py s 30
    Training for 30 seconds
    ...

    $> python trainer.py n 30
    Training for 30 iterations
    ...

    """

    # get args
    format_msg = "trainer.py [ {} | {} ] [ time_in_seconds | num_in_iterations ]".format(TIMECONST, NUMCONST)
    num_args = len(sys.argv)
    if num_args != 3:
        print(format_msg)
        return -1

    train_type = sys.argv[1]
    train_duration = int(sys.argv[2])

    if train_type == TIMECONST:
        print('Training for {} seconds'.format(train_duration))
        
        # train for train_duration seconds
        train_for(train_duration)

    elif train_type == NUMCONST:
        print('Training for {} iterations'.format(train_duration))

        # train for train_duration iterations
        train(train_duration)

    else:
        print(format_msg)

# test out trainer
if __name__ == "__main__":
    main(sys)
    


