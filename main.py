import pygame

WHITE = (255, 255, 255)
LIGHT_BLUE = (52, 152, 219)
LIGHT_RED = (231, 76, 60)
BLACK = (0, 0, 0)
FRAMES_PER_SECOND = 60
GAME_TITLE = 'ASS2 - Football Simulator - Controller'
GAME_SCREEN_SIZE = (1000, 500)
CIRCLE_RADIUS = 50
PLAYER_SHIFT = 10
clock = pygame.time.Clock()


# The Debugger class - use this class for printing out debugging information
class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode is "debug":
            print("> DEBUG: " + str(message))


class User:
    def __init__(self, user_color, players_initial_positions):
        self.color = user_color
        self.players_positions = players_initial_positions
        self.num_of_players = len(players_initial_positions)
        self.current_selected_player = 0


class GameManager:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.game_display = pygame.display.set_mode(GAME_SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)
        self.debugger = Debugger("debug")

    def start(self):
        loop = True
        is_user1_changed_player = False
        is_user2_changed_player = False
        # Initial values for handling players movement
        current_user1_player_cx = self.user1.players_positions[self.user1.current_selected_player][0]
        current_user1_player_cy = self.user1.players_positions[self.user1.current_selected_player][1]
        current_user1_player_shiftx = 0
        current_user1_player_shifty = 0
        current_user2_player_cx = self.user2.players_positions[self.user2.current_selected_player][0]
        current_user2_player_cy = self.user2.players_positions[self.user2.current_selected_player][1]
        current_user2_player_shiftx = 0
        current_user2_player_shifty = 0
        while loop:
            if is_user1_changed_player:
                current_user1_player_cx = self.user1.players_positions[self.user1.current_selected_player][0]
                current_user1_player_cy = self.user1.players_positions[self.user1.current_selected_player][1]
                is_user1_changed_player = False
            if is_user2_changed_player:
                current_user2_player_cx = self.user2.players_positions[self.user2.current_selected_player][0]
                current_user2_player_cy = self.user2.players_positions[self.user2.current_selected_player][1]
                is_user2_changed_player = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == pygame.KEYDOWN:
                    # User1 input handlers
                    if event.key == pygame.K_LSHIFT:
                        self.user1.current_selected_player = (self.user1.current_selected_player + 1) % self.user1.num_of_players
                        self.debugger.log("User1 is choosing player " + str(self.user1.current_selected_player))
                        is_user1_changed_player = True
                    if event.key == pygame.K_a:
                        current_user1_player_shiftx = -PLAYER_SHIFT
                        current_user1_player_shifty = 0
                    if event.key == pygame.K_d:
                        current_user1_player_shiftx = PLAYER_SHIFT
                        current_user1_player_shifty = 0
                    if event.key == pygame.K_w:
                        current_user1_player_shifty = -PLAYER_SHIFT
                        current_user1_player_shiftx = 0
                    if event.key == pygame.K_s:
                        current_user1_player_shifty = PLAYER_SHIFT
                        current_user1_player_shiftx = 0
                    # User2 input handlers
                    if event.key == pygame.K_RSHIFT:
                        self.user2.current_selected_player = (self.user2.current_selected_player + 1) % self.user2.num_of_players
                        self.debugger.log("User1 is choosing player " + str(self.user2.current_selected_player))
                        is_user2_changed_player = True
                    if event.key == pygame.K_LEFT:
                        current_user2_player_shiftx = -PLAYER_SHIFT
                        current_user2_player_shifty = 0
                    if event.key == pygame.K_RIGHT:
                        current_user2_player_shiftx = PLAYER_SHIFT
                        current_user2_player_shifty = 0
                    if event.key == pygame.K_UP:
                        current_user2_player_shifty = -PLAYER_SHIFT
                        current_user2_player_shiftx = 0
                    if event.key == pygame.K_DOWN:
                        current_user2_player_shifty = PLAYER_SHIFT
                        current_user2_player_shiftx = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_s or event.key == pygame.K_w:
                        current_user1_player_shiftx = 0
                        current_user1_player_shifty = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        current_user2_player_shiftx = 0
                        current_user2_player_shifty = 0
            if is_user1_changed_player or is_user2_changed_player:
                continue
            current_user1_player_cx += current_user1_player_shiftx
            current_user1_player_cy += current_user1_player_shifty
            current_user2_player_cx += current_user2_player_shiftx
            current_user2_player_cy += current_user2_player_shifty
            self.user1.players_positions[self.user1.current_selected_player] = (current_user1_player_cx, current_user1_player_cy)
            self.user2.players_positions[self.user2.current_selected_player] = (current_user2_player_cx, current_user2_player_cy)
            self.game_display.fill(WHITE)
            # Draw circle around selected players
            pygame.draw.circle(self.game_display, BLACK, self.user1.players_positions[self.user1.current_selected_player], CIRCLE_RADIUS + 10, 0)
            pygame.draw.circle(self.game_display, BLACK, self.user2.players_positions[self.user2.current_selected_player], CIRCLE_RADIUS + 10, 0)
            for player_position in self.user1.players_positions:
                pygame.draw.circle(self.game_display, self.user1.color, player_position, CIRCLE_RADIUS, 0)
            for player_position in self.user2.players_positions:
                pygame.draw.circle(self.game_display, self.user2.color, player_position, CIRCLE_RADIUS, 0)
            pygame.display.update()
            clock.tick(FRAMES_PER_SECOND)

# Run the main loop
user1 = User(LIGHT_BLUE, [(150, 250), (350, 150), (350, 350)])
user2 = User(LIGHT_RED, [(850, 250), (650, 150), (650, 350)])
my_game = GameManager(user1, user2)
my_game.start()
# Exit the game if the main loop ends
pygame.quit()
