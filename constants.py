__author__ = 'Hieu'

"""
Define some Global constants
"""


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BlUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLOR_KEY = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 657

# Frame per second
FPS = 60

# Play space
PLAY_SPACE_RECT = (85, 107, 831, 485)

# Ball start position
BALL_INIT_POS = (500, 350)

# Goal position
GOAL_LEFT_POS = (33, 266)
GOAL_RIGHT_POS = (941, 266)

# Players initial positions
USER1_PLAYERS_INITIAL_POS = [(200, 300), (375, 180), (375, 420)]
USER2_PLAYERS_INITIAL_POS = [(710, 300), (535, 180), (535, 420)]

# Button pos
GAMEOVER_BUTTON_POS = [
    (313, 471),
    (454, 471),
    (597, 471),
]

START_BUTTON_POS = [
    (563, 277),
    (233, 277),
    (443, 326)
]


GAMEOVER_BUTTON_TYPE = {"mute": 0, "replay": 1, "exit": 2}
GAMESTART_BUTTON_TYPE = {"exit": 0, "play": 1, "mute": 2}

SCORE_COLOR = (9, 103, 19)
SCORE_POS = (500, 240)
TROPHY_POS = [
    (235, 290),
    (545, 290)
]