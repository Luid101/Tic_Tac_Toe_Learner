import pygame, sys, random
from AI import AI as TicTacToeAI

class TicTacToe:
    SYMBOLS = ['x', 'o']

    def __init__(self):
        pygame.init()
        self._font = pygame.font.SysFont("monospace", 40)
        self._message = pygame.font.SysFont("monospace", 15)
        self._turn = 0  # Number of turns so far
        self._game_array = {(0, 0): '-', (225, 0): '-', (450, 0): '-',
                            (0, 225): '-', (225, 225): '-', (450, 225): '-',
                            (0, 450): '-', (225, 450): '-', (450, 450): '-'}
        self._x_image = pygame.image.load("images/x.png")
        self._o_image = pygame.image.load("images/o.png")
        self._x_image_small = pygame.transform.scale(self._x_image, (100, 100))
        self._o_image_small = pygame.transform.scale(self._o_image, (100, 100))
        self._game_display = pygame.display.set_mode((1000, 650))
        self._ai = TicTacToeAI()
        self._player_num = 0
        self._ai_num = 1
        self._player_score = 0
        self._ai_score = 0
        self._won = False
        self._current_win_state = False
        self._previous_win_state = False
        self._winner = None
        self._ai_learn_msg = None

    def process_click(self, mouse_coords):
        """
        Processes your clicks and stores x/o into the game array
        :param mouse_coords (tuple(int)): coordinates
        :return: None
        """
        if 0 <= mouse_coords[0] <= 199:
            # First row
            if 0 <= mouse_coords[1] <= 199 and self._game_array[(0, 0)] == '-':
                # First column
                self._game_array[(0, 0)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

            elif 225 <= mouse_coords[1] <= 424 and \
                    self._game_array[(0, 225)] == '-':
                # Second column
                self._game_array[(0, 225)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

            elif 450 <= mouse_coords[1] <= 649 and \
                    self._game_array[(0, 450)] == '-':
                # Third column
                self._game_array[(0, 450)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

        elif 225 <= mouse_coords[0] <= 424:
            # Second row
            if 0 <= mouse_coords[1] <= 199 and \
                    self._game_array[(225, 0)] == '-':
                # First column
                self._game_array[(225, 0)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

            elif 225 <= mouse_coords[1] <= 424 and \
                    self._game_array[(225, 225)] == '-':
                # Second column
                self._game_array[(225, 225)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

            elif 450 <= mouse_coords[1] <= 649 and \
                    self._game_array[(225, 450)] == '-':
                # Third column
                self._game_array[(225, 450)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

        elif 450 <= mouse_coords[0] <= 649:
            # Third row
            if 0 <= mouse_coords[1] <= 199 and \
                    self._game_array[(450, 0)] == '-':
                # First column
                self._game_array[(450, 0)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

            elif 225 <= mouse_coords[1] <= 424 and \
                    self._game_array[(450, 225)] == '-':
                # Second column
                self._game_array[(450, 225)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

            elif 450 <= mouse_coords[1] <= 649 and \
                    self._game_array[(450, 450)] == '-':
                # Third column
                self._game_array[(450, 450)] = self.SYMBOLS[self._player_num]
                self._turn += 1  # Next turn

    def reset(self, mouse_coords):
        if 650 <= mouse_coords[0] <= 1000:
            # Reset
            if '-' not in self._game_array.values():
                self._ai.has_drawn()
            if 550 <= mouse_coords[1] <= 650:     
                self._turn = 0
                self._won = False
                self._current_win_state = False
                self._previous_win_state = False
                self._player_num, self._ai_num = self._ai_num, self._player_num
                for coords in self._game_array:
                    self._game_array[coords] = '-'

    def draw_board(self, game_display):
        # Draws the board
        game_display.fill((255, 255, 255))
        pygame.draw.rect(game_display, (0, 0, 0), (200, 0, 25, 650), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (425, 0, 25, 650), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (0, 200, 650, 25), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (0, 425, 650, 25), 0)
        pygame.draw.rect(game_display, (255, 105, 180), (650, 550, 350, 100), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (650, 0, 10, 650), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (650, 550, 350, 10), 0)

        # Draws the X's and O's
        for coords in self._game_array:
            if self._game_array[coords] == 'x':
                game_display.blit(self._x_image, coords)
            elif self._game_array[coords] == 'o':
                game_display.blit(self._o_image, coords)

        player_label = self._font.render("Player", 1, (0, 0, 0))
        game_display.blit(player_label, (680, 10))
        ai_label = self._font.render("AI", 1, (0, 0, 0))
        game_display.blit(ai_label, (680, 200))

        if self._player_num == 0:
            game_display.blit(self._x_image_small, (680, 50))
            game_display.blit(self._o_image_small, (680, 240))
        else:
            game_display.blit(self._o_image_small, (680, 50))
            game_display.blit(self._x_image_small, (680, 240))

        player_score_label = self._font.render(str(self._player_score), 1,
                                               (0, 0, 0))
        game_display.blit(player_score_label, (900, 10))
        ai_score_label = self._font.render(str(self._ai_score), 1,
                                               (0, 0, 0))
        game_display.blit(ai_score_label, (900, 200))

        reset_label = self._font.render("Reset", 1, (0, 0, 0))
        game_display.blit(reset_label, (770, 580))

        if self._won:
            winner_label = self._message.render(self._winner + " won!", 1,
                                                (0, 0, 0))
            message = self._message.render(self._ai_learn_msg, 1, (0, 0, 0))
            game_display.blit(winner_label, (660, 400))
            game_display.blit(message, (660, 450))

    def win(self, symbol):
        """
        Determines whether player symbol has won
        :param symbol: 'x' or 'o'
        :return: True if player has won, False otherwise
        """
        a = self._game_array  # More convenient name
        if all(x == symbol for x in [a[(0, 0)], a[(0, 225)], a[(0, 450)]]):
            return True
        elif all(x == symbol for x in [a[(225, 0)], a[(225, 225)],
                                       a[(225, 450)]]):
            return True
        elif all(x == symbol for x in [a[(450, 0)], a[(450, 225)],
                                       a[(450, 450)]]):
            return True
        elif all(x == symbol for x in [a[(0, 0)], a[(225, 0)],
                                       a[(450, 0)]]):
            return True
        elif all(x == symbol for x in [a[(0, 225)], a[(225, 225)],
                                           a[(450, 225)]]):
            return True
        elif all(x == symbol for x in [a[(0, 450)], a[(225, 450)],
                                       a[(450, 450)]]):
            return True
        elif all(x == symbol for x in [a[(0, 0)], a[(225, 225)],
                                       a[(450, 450)]]):
            return True
        elif all(x == symbol for x in [a[(0, 450)], a[(225, 225)],
                                       a[(450, 0)]]):
            return True
        else:
            return False

    def ai_input(self):
        positions = [(0, 0), (225, 0), (450, 0), (0, 225), (225, 225),
                     (450, 225), (0, 450), (225, 450), (450, 450)]
        a = self._game_array  # Less annoying name
        current_board = [a[(0, 0)], a[(225, 0)], a[(450, 0)], a[(0, 225)],
                         a[(225, 225)], a[(450, 225)], a[(0, 450)],
                         a[(225, 450)], a[(450, 450)]]
        for i in range(0, 9):
            # Replace the symbols in the array with symbols that can be read by
            # the AI
            sym = 0
            if (current_board[i] == 'x' and self._player_num == 0) or \
                (current_board[i] == 'o' and self._player_num == 1):
                sym = 1
            elif (current_board[i] == 'x' and self._ai_num == 0) or \
                (current_board[i] == 'o' and self._ai_num == 1):
                sym = 2
            current_board[i] = sym

        print(current_board)

        new_move = self._ai.move(current_board)
        print(new_move)
        self._game_array[positions[new_move]] = self.SYMBOLS[self._ai_num]
        self._turn += 1

    def run(self):
        # Sets up GUI
        pygame.display.set_caption("Thicc Tac Toe")
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self._won \
                    and self._turn < 9 and self._turn % 2 == self._player_num:
                    self.process_click(pygame.mouse.get_pos())
                elif not self._won and self._turn < 9 \
                    and self._turn % 2 == self._ai_num:
                    self.ai_input()
                elif event.type == pygame.MOUSEBUTTONDOWN and (self._turn > 8
                                                               or self._won):
                    self.reset(pygame.mouse.get_pos())

            self.draw_board(self._game_display)
            pygame.display.update()
            x_win = self.win('x')
            o_win = self.win('o')
            self._won = x_win or o_win
            self._current_win_state = x_win or o_win
            if self._current_win_state != self._previous_win_state and \
                self._current_win_state:
                # Rising edge, change from no win to win, same concept as CSC258
                if (x_win and self._player_num == 0) or \
                    (o_win and self._player_num == 1):
                    self._ai_learn_msg = self._ai.has_lost()
                    print("Player won")
                    self._player_score += 1
                    self._winner = "Player"
                elif (x_win and self._ai_num == 0) or \
                        (o_win and self._ai_num == 1):
                    self._ai_learn_msg = self._ai.has_won()
                    print("AI won")
                    self._ai_score += 1
                    self._winner = "AI"
            self._previous_win_state = self._current_win_state
            clock.tick(60)

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
