class Board:
    def __init__(self):

        self.first_row = [' ', ' ', ' ']
        self.second_row = [' ', ' ', ' ']
        self.third_row = [' ', ' ', ' ']
        self.rows = [self.first_row, self.second_row, self.third_row]
        self.x_turn = True
        self.initial_state = True

    def update_turn(self):
        if (self.x_turn):
            self.x_turn = False
        else:
            self.x_turn = True

    def make_move(self, x, y):
        self.initial_state = False
        if (self.x_turn):
            self.rows[y][x] = 'X'
        else:
            self.rows[y][x] = 'O'
        self.update_turn()

    def has_won(self):
        if not self.initial_state:
            return ((self.rows[0][0] == self.rows[0][1] and self.rows[0][2] == self.rows[0][1] and (not self.rows[0][2] == ' ')) or
                    (self.rows[1][0] == self.rows[1][1] and self.rows[1][2] == self.rows[1][1] and (not self.rows[0][2] == ' ')) or
                    (self.rows[2][0] == self.rows[2][1] and self.rows[2][2] == self.rows[2][1] and (not self.rows[0][2] == ' ')) or
                    (self.rows[0][0] == self.rows[1][0] and self.rows[2][0] == self.rows[1][0] and (not self.rows[0][2] == ' ')) or
                    (self.rows[0][1] == self.rows[1][1] and self.rows[2][1] == self.rows[1][1] and (not self.rows[0][2] == ' ')) or
                    (self.rows[0][2] == self.rows[1][2] and self.rows[2][2] == self.rows[1][2] and (not self.rows[0][2] == ' ')) or
                    (self.rows[0][0] == self.rows[1][1] and self.rows[2][2] == self.rows[1][1] and (not self.rows[0][2] == ' ')) or
                    (self.rows[0][2] == self.rows[1][1] and self.rows[2][0] == self.rows[1][1] and (not self.rows[0][2] == ' ')))

    def user_turn(self):
        self.generate_board()
        if self.x_turn:
            user_input = input("PLAYER X, GIVE YOUR DESIRED POSITION: ").strip()
        elif not self.x_turn:
            user_input = input("PLAYER O, GIVE YOU DESIRED POSITION: ").strip()
        if (len(user_input) == 3) and (user_input[1] == ',') and (user_input[0] in '123') \
            and (user_input[2] in '123'):
            x = int(user_input[0])
            y = int(user_input[2])

            self.make_move(x,y)


    def generate_board(self):
        print('      ||      ||')
        print(' ' + self.first_row[0] + '    || ' + self.first_row[1] + '    || ' + self.first_row[2])
        print('      ||      ||')
        print('======================')
        print('      ||      ||')
        print(' ' + self.second_row[0] + '    || ' + self.second_row[1] + '    || ' + self.second_row[2])
        print('      ||      ||')
        print('======================')
        print('      ||      ||')
        print(' ' + self.third_row[0] + '    || ' + self.third_row[1] + '    || ' + self.third_row[2])
        print('      ||      ||')












