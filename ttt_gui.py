import pygame, sys
from ttt_controller import TicTacToeController, Player
from AI import AI

class TicTacToeGUI:
    """
    GUI for Tic Tac Toe using Pygame
    """
    def __init__(self, controller, window_name="Tic Tac Toe"):
        """
        :param controller: Tic Tac Toe controller
        :param window_name: Name of the game window
        :return: None
        """
        self._controller = controller
        pygame.init()
        pygame.display.set_caption(window_name)
        self._clock = pygame.time.Clock()
        self._found_result = False
        self._display = pygame.display.set_mode((1000, 650))
        self._x_image = pygame.image.load("images/x.png")
        self._o_image = pygame.image.load("images/o.png")
        self._board_coordinates = [(0, 0), (225, 0), (450, 0),
                                   (0, 225), (225, 225), (450, 225),
                                   (0, 450), (225, 450), (450, 450)]

    def draw_board(self):
        self._display.fill((255, 255, 255))  # White background
        # Grid
        pygame.draw.rect(self._display, (0, 0, 0), (200, 0, 25, 650))
        pygame.draw.rect(self._display, (0, 0, 0), (425, 0, 25, 650))
        pygame.draw.rect(self._display, (0, 0, 0), (0, 200, 650, 25))
        pygame.draw.rect(self._display, (0, 0, 0), (0, 425, 650, 25))
        pygame.draw.rect(self._display, (0, 0, 0), (650, 0, 10, 650))

        # Reset button
        pygame.draw.rect(self._display, (255, 105, 180), (650, 550, 350, 100))
        pygame.draw.rect(self._display, (0, 0, 0), (650, 550, 10, 650))
        pygame.draw.rect(self._display, (0, 0, 0), (650, 550, 350, 10))
        reset_label = pygame.font.SysFont("monospace", 40).\
            render("Reset", 1, (0, 0, 0))
        self._display.blit(reset_label, (770, 580))

        # Player 1 label and score
        player_1_label = pygame.font.SysFont("monospace", 40).\
            render(self._controller.get_player1().get_name(), 1, (0, 0, 0))
        player_1_score = pygame.font.SysFont("monospace", 40).\
            render(str(self._controller.get_player1().get_score()),
                   1, (0, 0, 0))
        self._display.blit(player_1_label, (680, 10))
        self._display.blit(player_1_score, (900, 10))

        # Player 2 label and score
        player_2_label = pygame.font.SysFont("monospace", 40).\
            render(self._controller.get_player2().get_name(), 1, (0, 0, 0))
        player_2_score = pygame.font.SysFont("monospace", 40).\
            render(str(self._controller.get_player2().get_score()),
                   1, (0, 0, 0))
        self._display.blit(player_2_label, (680, 200))
        self._display.blit(player_2_score, (900, 200))

        # Symbols
        for i in range(0, 9):
            if self._controller.get_board()[i] == 'x':
                self._display.blit(self._x_image, self._board_coordinates[i])
            elif self._controller.get_board()[i] == 'o':
                self._display.blit(self._o_image, self._board_coordinates[i])

    def process_click(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]

        if x in range(0, 201):  # First column
            print("Test")
            if y in range(0, 201):  # First row
                print("Hi")
                self._controller.move(0)
            elif y in range(225, 426):  # Second row
                self._controller.move(3)
            elif y in range(450, 651):  # Third row
                self._controller.move(6)

        elif x in range(225, 426):  # Second column
            if y in range(0, 201):  # First row
                self._controller.move(1)
            elif y in range(225, 426):  # Second row
                self._controller.move(4)
            elif y in range(450, 651):  # Third row
                self._controller.move(7)

        elif x in range(450, 651):  # Third column
            if y in range(0, 201):  # First row
                self._controller.move(2)
            elif y in range(225, 426):  # Second row
                self._controller.move(5)
            elif y in range(450, 651):  # Third row
                self._controller.move(8)

        elif x in range(650, 1001) and y in range(550, 651):
            # Reset "button" that's not really a button it's so ghetto
            self._found_result = True
            self._controller.reset()

    def run(self):
        """
        :return:
        """
        current_player = self._controller.get_current_player()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit game
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If a human clicks or if the current player is an AI
                    self.process_click(pygame.mouse.get_pos())
                    print(self._controller.get_board())
                    print(self._controller.get_turns())
                    print(self._controller.get_is_done())
                elif current_player.get_mode() == 1:
                    self.process_click((0, 0))
                print(event)

            self.draw_board()
            pygame.display.flip()
            pygame.display.update()
            if not self._found_result:
                # Prevents from checking whether a player won or game ended in
                # a tie because game runs in a loop.
                self._found_result = True if self._controller.win() or \
                    self._controller.tie() else False
            self._clock.tick(60)

if __name__ == "__main__":
    human = Player(0, 1, "Human")
    ai = Player(1, 2, "AI", AI())
    controller = TicTacToeController(human, ai)
    gui = TicTacToeGUI(controller)
    gui.run()
