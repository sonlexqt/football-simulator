__author__ = 'Hieu'
"""
Starting point of game
"""
from game_manager import *

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()
game_manager = GameManager()
game_manager.start(True)

