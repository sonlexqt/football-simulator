__author__ = 'Hieu'
"""
Implement player/player sprite
"""
import pygame
from sprite_factory import SpriteFactory
from collision import Collision
from event_handlers import *


class Player(pygame.sprite.Sprite):

    def __init__(self, manager, sprite, frame_data, player_initial_position, ball, sfx):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.change_x = 0
        self.change_y = 0
        self.frames = []
        self.manager = manager
        player_frames = SpriteFactory.generate_frames(sprite, frame_data)
        image = player_frames[0]
        self.frames.append(image)
        self.manager.add(self)
        # Set the image the player starts with
        self.image = self.frames[0]
        # Set a reference to the image rect
        self.rect = self.image.get_rect()
        # self.center = self.rect.width / 2, self.rect.height / 2
        self.rect.x = player_initial_position[0]
        self.rect.y = player_initial_position[1]
        self.radius = 37
        self.m = 50
        self.collision = Collision()
        self.ball = ball
        self.player_list = []
        self.sfx = sfx
        self.player_vs_ball_observable = PlayerVsBallObservable()
        self.player_vs_ball_observer = PlayerVsBallObserver(sfx)
        self.player_vs_ball_observable.register(self.player_vs_ball_observer)
        self.direction = [0, 0]

    def update(self):
        # Move left/right/up/down
        self.collision.collisionPlayer2Wall(self)
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.collision.collisionPlayer2Ball(self, self.ball, self.player_vs_ball_observable)

    def go_left(self):
        self.change_x = -6
        self.change_y = 0

    def go_right(self):
        self.change_x = 6
        self.change_y = 0

    def go_up(self):
        self.change_y = -6
        self.change_x = 0

    def go_down(self):
        self.change_y = 6
        self.change_x = 0

    def stop(self):
        self.change_x = 0
        self.change_y = 0
    def getPlayerList(self, player_list):
        self.player_list = player_list