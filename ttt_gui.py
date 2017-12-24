import pygame, sys
from ttt_controller import TicTacToeController, Player
from AI import AI


class TicTacToeGUI:
    """
    GUI for Tic Tac Toe using Pygame
    :ivar _board_coordinates: Coordinates of each symbol on the board
    :ivar _controller: Tic Tac Toe controller
    :ivar _clock: Pygame clock
    :ivar _display: Pygame display
    :ivar _found_result: True if a game is done, False otherwise
    :ivar _o_image: o
    :ivar _x_image: x
    """
    def __init__(self, controller, window_name="Tic Tac Toe"):
        """
        :param controller: Tic Tac Toe controller
        :param window_name: Name of the game window
        :return: None
        """
        self._controller = controller
        self._found_result = False
        pygame.init()
        pygame.display.set_caption(window_name)
        self._clock = pygame.time.Clock()
        self._display = pygame.display.set_mode((1000, 650))
        self._x_image = pygame.image.load("images/x.png")
        self._o_image = pygame.image.load("images/o.png")
        self._board_coordinates = [(0, 0), (225, 0), (450, 0),
                                   (0, 225), (225, 225), (450, 225),
                                   (0, 450), (225, 450), (450, 450)]

    def draw_board(self):
        """
        Draws the board
        :return: None
        """
        self._display.fill((255, 255, 255))  # White background
        self.draw_grid()
        self.draw_reset()
        self.draw_player_labels()
        self.draw_symbols()
        self.draw_game_over_message()

    def draw_game_over_message(self):
        """
        Draws message when the game is over
        :return: None
        """
        if self._controller.get_is_done() and self._found_result:
            game_over_message = None
            if self._controller.get_is_win():
                # Displays winner
                winner = self._controller.get_winner()
                game_over_message = pygame.font.SysFont("monospace", 15).\
                    render(winner.get_name() + " won!", 1, (0, 0, 0))
            elif self._controller.get_is_tie():
                game_over_message = pygame.font.SysFont("monospace", 15).\
                    render("Game ended in a tie", 1, (0, 0, 0))

            self._display.blit(game_over_message, (665, 450))
            # Displays message from player 1 if player 1 is an AI
            if self._controller.get_player1().get_mode() == 1:
                p1_message = pygame.font.SysFont("monospace", 15).\
                    render(self._controller.get_player1()
                           .get_ai_message(), 1, (0, 0, 0))
                self._display.blit(p1_message, (665, 475))

            # Displays message from player 2 if player 2 is an AI
            if self._controller.get_player2().get_mode() == 1:
                p2_message = pygame.font.SysFont("monospace", 15).\
                    render(self._controller.get_player2()
                           .get_ai_message(), 1, (0, 0, 0))
                self._display.blit(p2_message, (665, 500))

    def draw_grid(self):
        """
        Draws the grid
        :return: None
        """
        pygame.draw.rect(self._display, (0, 0, 0), (200, 0, 25, 650))
        pygame.draw.rect(self._display, (0, 0, 0), (425, 0, 25, 650))
        pygame.draw.rect(self._display, (0, 0, 0), (0, 200, 650, 25))
        pygame.draw.rect(self._display, (0, 0, 0), (0, 425, 650, 25))
        pygame.draw.rect(self._display, (0, 0, 0), (650, 0, 10, 650))

    def draw_player_labels(self):
        """
        Draws player labels, symbols, and scores
        :return: None
        """
        player1 = self._controller.get_player1()
        player2 = self._controller.get_player2()
        player_order = self._controller.get_players()

        player_1_label = pygame.font.SysFont("monospace", 40).\
            render(player1.get_name(), 1, (0, 0, 0))
        player_1_score = pygame.font.SysFont("monospace", 40).\
            render(str(player1.get_score()), 1, (0, 0, 0))
        self._display.blit(player_1_label, (680, 10))
        self._display.blit(player_1_score, (900, 10))

        # Player 2 label and score
        player_2_label = pygame.font.SysFont("monospace", 40).\
            render(player2.get_name(), 1, (0, 0, 0))
        player_2_score = pygame.font.SysFont("monospace", 40).\
            render(str(player2.get_score()), 1, (0, 0, 0))
        self._display.blit(player_2_label, (680, 200))
        self._display.blit(player_2_score, (900, 200))

        # draw the number of draws
        draws_label = pygame.font.SysFont("monospace", 40).\
            render("Draws", 1, (0, 0, 0))
        draws_amount = pygame.font.SysFont("monospace", 40).\
            render(str(controller.get_draws()), 1, (0, 0, 0))
        self._display.blit(draws_label, (680, 360))
        self._display.blit(draws_amount, (900, 360))

        if player1 == player_order[0]:
            # Player 1 is x, Player 2 is o
            self._display.blit(pygame.transform.scale(
                self._x_image, (100, 100)), (680, 50))
            self._display.blit(pygame.transform.scale(
                self._o_image, (100, 100)), (680, 240))
        else:
            # Player 1 is o, Player 2 is x
            self._display.blit(pygame.transform.scale(
                self._o_image, (100, 100)), (680, 50))
            self._display.blit(pygame.transform.scale(
                self._x_image, (100, 100)), (680, 240))

    def draw_reset(self):
        """
        Draws the reset button
        :return: None
        """
        pygame.draw.rect(self._display, (255, 105, 180), (650, 550, 350, 100))
        pygame.draw.rect(self._display, (0, 0, 0), (650, 550, 10, 650))
        pygame.draw.rect(self._display, (0, 0, 0), (650, 550, 350, 10))
        reset_label = pygame.font.SysFont("monospace", 40).render("Reset",
                                                                  1, (0, 0, 0))
        self._display.blit(reset_label, (770, 580))

    def draw_symbols(self):
        """
        Draws game symbols
        :return: None
        """
        for i in range(0, 9):
            if self._controller.get_board()[i] == 'x':
                self._display.blit(self._x_image, self._board_coordinates[i])
            elif self._controller.get_board()[i] == 'o':
                self._display.blit(self._o_image, self._board_coordinates[i])

    def process_click(self, mouse_pos):
        """
        Processes human/AI input
        :param mouse_pos: mouse coordinates
        :return: None
        """
        x = mouse_pos[0]
        y = mouse_pos[1]
        human_input = self._controller.get_current_player().get_mode() == 0
        ai_input = self._controller.get_current_player().get_mode() == 1
        done = self._controller.get_is_done()

        if human_input and not done:
            # Human input
            if x in range(0, 201):  # First column
                if y in range(0, 201):  # First row
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

        elif ai_input and not done:
            # AI input
            self._controller.move(0)

        elif done:
            # Reset
            if x in range(650, 1001) and y in range(550, 651):
                # Reset "button" that's not really a button it's so ghetto
                self._found_result = False
                self._controller.reset()

    def run(self):
        """
        Runs the program
        :return: None
        """
        while True:
            # More convenient names
            current_mode = self._controller.get_current_player().get_mode()

            for event in pygame.event.get():
                # More convenient names
                game_not_over = (event.type == pygame.MOUSEBUTTONDOWN or
                    current_mode == 1) and not self._controller.get_is_done()
                game_over = event.type == pygame.MOUSEBUTTONDOWN and \
                    self._controller.get_is_done()

                if event.type == pygame.QUIT:
                    # Exit game
                    pygame.quit()
                    sys.exit(0)
                elif game_not_over or game_over:
                    # If a human clicks or if the current player is an AI, or
                    # the game is over
                    self.process_click(pygame.mouse.get_pos())

            self.draw_board()
            pygame.display.flip()
            pygame.display.update()
            if not self._found_result:
                # Prevents from checking whether a player won or game ended in
                # a tie multiple times because game runs in a loop.
                self._controller.set_game_over()
                if self._controller.get_is_win() or \
                        self._controller.get_is_tie():
                    self._found_result = True
            self._clock.tick(60)

if __name__ == "__main__":
    human = Player(0, 1, "Human")
    ai = Player(1, 2, "AI", AI())
    controller = TicTacToeController(human, ai)
    gui = TicTacToeGUI(controller, "Thicc Tac Toe")
    gui.run()