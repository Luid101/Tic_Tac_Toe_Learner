import pygame, sys

class TicTacToeGui:
    SYMBOLS = ['X', 'O']

    def __init__(self):
        self._turn = 0  # Number of turns so far
        self._game_array = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def run(self):
        pygame.init()

        # Sets up GUI
        game_display = pygame.display.set_mode((650, 650))
        pygame.display.set_caption("Thicc Tac Toe")
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                print(event)

            # Draws the board
            game_display.fill((255, 255, 255))
            pygame.draw.rect(game_display, (0, 0, 0), (200, 0, 25, 700), 0)
            pygame.draw.rect(game_display, (0, 0, 0), (425, 0, 25, 700), 0)
            pygame.draw.rect(game_display, (0, 0, 0), (0, 200, 700, 25), 0)
            pygame.draw.rect(game_display, (0, 0, 0), (0, 425, 700, 25), 0)

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    gui = TicTacToeGui()
    gui.run()
