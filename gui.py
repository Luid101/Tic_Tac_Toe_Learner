import pygame, sys
import random

class TicTacToe:
    SYMBOLS = ['x', 'o']

    def __init__(self):
        pygame.init()
        self._turn = 0  # Number of turns so far
        self._game_array = {(0, 0): '-', (225, 0): '-', (450, 0): '-',
                            (0, 225): '-', (225, 225): '-', (450, 225): '-',
                            (0, 450): '-', (225, 450): '-', (450, 450): '-'}
        self._x_image = pygame.image.load("images/x.png")
        self._o_image = pygame.image.load("images/o.png")
        self._game_display = pygame.display.set_mode((850, 650))

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
                self._game_array[(0, 0)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

            elif 225 <= mouse_coords[1] <= 424 and \
                    self._game_array[(0, 225)] == '-':
                # Second column
                self._game_array[(0, 225)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

            elif 450 <= mouse_coords[1] <= 699 and \
                    self._game_array[(0, 450)] == '-':
                # Third column
                self._game_array[(0, 450)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

        elif 225 <= mouse_coords[0] <= 424:
            # Second row
            if 0 <= mouse_coords[1] <= 199 and \
                    self._game_array[(225, 0)] == '-':
                # First column
                self._game_array[(225, 0)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

            elif 225 <= mouse_coords[1] <= 424 and \
                    self._game_array[(225, 225)] == '-':
                # Second column
                self._game_array[(225, 225)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

            elif 450 <= mouse_coords[1] <= 699 and \
                    self._game_array[(225, 450)] == '-':
                # Third column
                self._game_array[(225, 450)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

        elif 450 <= mouse_coords[0] <= 699:
            # Third row
            if 0 <= mouse_coords[1] <= 199 and \
                    self._game_array[(450, 0)] == '-':
                # First column
                self._game_array[(450, 0)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

            elif 225 <= mouse_coords[1] <= 424 and \
                    self._game_array[(450, 225)] == '-':
                # Second column
                self._game_array[(450, 225)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

            elif 450 <= mouse_coords[1] <= 699 and \
                    self._game_array[(450, 450)] == '-':
                # Third column
                self._game_array[(450, 450)] = self.SYMBOLS[self._turn % 2]
                self._turn += 1  # Next turn

    def draw_board(self, game_display):
        # Draws the board
        game_display.fill((255, 255, 255))
        pygame.draw.rect(game_display, (0, 0, 0), (200, 0, 25, 650), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (425, 0, 25, 650), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (0, 200, 650, 25), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (0, 425, 650, 25), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (650, 0, 10, 650), 0)

        # Draws the X's and O's
        for coords in self._game_array:
            if self._game_array[coords] == 'x':
                game_display.blit(self._x_image, coords)
            elif self._game_array[coords] == 'o':
                game_display.blit(self._o_image, coords)

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
        positions = list(self._game_array.keys())
        found = False
        if self._turn % 2 == 1 and self._turn < 9:
            while not found:
                random_pos = random.choice(positions)
                if self._game_array[random_pos] == '-':
                    found = True
                    self._game_array[random_pos] = self.SYMBOLS[self._turn % 2]
                    self._turn += 1

    def run(self):
        # Sets up GUI
        pygame.display.set_caption("Thicc Tac Toe")
        clock = pygame.time.Clock()
        won = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and not won \
                        and self._turn < 9 and self._turn % 2 == 0:
                    self.process_click(pygame.mouse.get_pos())
                elif not won and self._turn < 9 and self._turn % 2 == 1:
                    self.ai_input()

            self.draw_board(self._game_display)
            pygame.display.update()
            x_win = self.win('x')
            o_win = self.win('o')
            won = x_win or o_win
            clock.tick(60)

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
