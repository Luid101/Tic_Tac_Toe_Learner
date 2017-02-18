import pygame, sys

class TicTacToeGui:
    SYMBOLS = ['x', 'o']

    def __init__(self):
        pygame.init()
        self._turn = 0  # Number of turns so far
        self._game_array = {(0, 0): '-', (225, 0): '-', (450, 0): '-',
                            (0, 225): '-', (225, 225): '-', (450, 225): '-',
                            (0, 450): '-', (225, 450): '-', (450, 450): '-'}
        self._x_image = pygame.image.load("images/x.png")
        self._o_image = pygame.image.load("images/o.png")

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
        pygame.draw.rect(game_display, (0, 0, 0), (200, 0, 25, 700), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (425, 0, 25, 700), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (0, 200, 700, 25), 0)
        pygame.draw.rect(game_display, (0, 0, 0), (0, 425, 700, 25), 0)

        # Draws the X's and O's
        for coords in self._game_array:
            if self._game_array[coords] == 'x':
                game_display.blit(self._x_image, coords)
            elif self._game_array[coords] == 'o':
                game_display.blit(self._o_image, coords)

    def run(self):
        # Sets up GUI
        game_display = pygame.display.set_mode((650, 650))
        pygame.display.set_caption("Thicc Tac Toe")
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.process_click(pygame.mouse.get_pos())

            self.draw_board(game_display)
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    gui = TicTacToeGui()
    gui.run()
