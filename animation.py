__author__ = 'Hieu'

import pygame
import constants
import math
from collision import Collision
from event_handlers import *


class Animation(pygame.sprite.Sprite):
    INFINITE = 0

    # @parameters:
    #   manager: pygame.sprite.Group that manages the sprite (add, remove, kill)
    #   frame: list of frame of the animation of effect
    #   speed: (millisecond) time needed for each animation loop
    def __init__(self, manager, frames, speed=1000):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.frames = frames
        self.frameLength = len(self.frames)
        self.currentFrame = 0
        self.image = self.frames[self.currentFrame]
        self.rect = self.image.get_rect()
        self.speed = speed
        self.fps = 1
        self.counter = 0
        self.finished = True
        self.times = 1
        self.origin_frame = Animation.copy_frame(self.frames)
        self.degree = 0
        self.is_static = False

    def add_frame(self, fr):
        self.frames.append(fr)

    def update(self):
        # Increase relative frame per second
        self.update_relative_fps()
        # Only play as much as ordered
        if (self.counter >= self.times) and self.times is not self.INFINITE:
            self.finished = True
            self.manager.remove(self)
        # Because of given speed, only shift the frame in the right time and when the loop not finish yet
        if self.is_time_to_update() and not self.finished:
            self.currentFrame = (self.currentFrame + self.calc_frame_step()) % self.frameLength
            self.image = self.frames[self.currentFrame]
        # Trigger increasing counter when loop finish a cycle
        if self.currentFrame == (self.frameLength - 1):
            self.counter += 1
            self.currentFrame = 0

    def calc_frame_step(self):
        return 1

    def play(self, times=1):
        self.finished = False
        self.times = times
        self.counter = 0
        self.manager.add(self)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_position_center(self, x, y):
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2

    def update_relative_fps(self):
        self.fps += 1

    def is_time_to_update(self):
        if self.is_static:
            return False
        if self.fps > constants.FPS / ((self.frameLength / self.speed) * 1000):
            self.fps = 1
            return True
        return False

    def rotate_more(self, deg):
        absolute_deg = self.degree + deg
        self.degree = absolute_deg
        for i in range(0, len(self.frames), 1):
            self.frames[i] = Animation.rot_center(self.origin_frame[i], absolute_deg)

    def rotate(self, deg):
        for i in range(0, len(self.frames), 1):
            self.frames[i] = Animation.rot_center(self.origin_frame[i], deg)

    @staticmethod
    def rot_center(image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    @staticmethod
    def copy_frame(frames):
        new_frame = []
        for i in range(0, len(frames), 1):
            new_frame.append(frames[i].copy())
        return new_frame


# The effect occur when a player is active - controlled by user
class FocusEffect(Animation):
    def __init__(self, manager, player, frame, speed=1000):
        Animation.__init__(self, manager, frame, speed)
        self.player = player

    def update(self):
        Animation.update(self)
        center = self.player.rect.center
        # self.set_position(rect.x + rect.width/2, rect.y + rect.height/2)
        self.set_position_center(center[0], center[1])

    def set_player(self, player):
        self.player = player


class Ball(Animation):
    BALL_STOP_BOUND = 1.3
    MAX_VELOCITY = 10

    def __init__(self, manager, position, frame, sfx, speed=1000):
        Animation.__init__(self, manager, frame, speed)
        self.collision = Collision()
        self.set_position_center(position[0], position[1])
        self.change_x = 0
        self.change_y = 0
        self.radius = 15.5
        self.is_ball_going_in = False
        self.is_ball_hit_wall = False
        self.goal = False
        self.m = 0.45
        self.prevent = 1.01
        self.ball_vs_wall_observable = BallVsWallObservable()
        self.ball_vs_wall_observer = BallVsWallObserver(sfx)
        self.ball_vs_wall_observable.register(self.ball_vs_wall_observer)

    def calc_frame_step(self):
        cx = math.fabs(self.change_x)
        cy = math.fabs(self.change_y)
        if max(cx, cy) == 0:
            return 1
        # elif 2 >= cx > 0.6 or 2 >= cy > 0.6:
        #     return 1
        elif 4 > cx > 2 or 4 > cy > 2:
            self.speed = 1000
            return 2
        elif 5 > cx >= 4 or 5 > cy >= 4:
            self.speed = 1000
            return 3
        elif cx >= 5 or cy >= 5:
            self.speed = 1000
            return 4
        else:
            self.speed = int(1000 * 0.5 / (self.change_x + self.change_y))
            # self.speed = 1000 - 80 / (self.change_x + self.change_y)
            return 1

    def update(self):
        if self.change_x + self.change_y == 0:
            self.is_static = True
        else:
            self.is_static = False
        Animation.update(self)
        if (self.rect.center[1] + self.change_y < constants.PLAY_SPACE_RECT[1] or self.rect.center[1] + self.change_y >
                constants.PLAY_SPACE_RECT[1] + constants.PLAY_SPACE_RECT[3]):
            self.change_y = 0
        # if ((self.rect.center[0] + self.change_x < constants.PLAY_SPACE_RECT[0] or self.rect.center[0] + self.change_x >
        #         constants.PLAY_SPACE_RECT[0] + constants.PLAY_SPACE_RECT[2]) \
        #             and (self.rect.center[1] - self.radius + self.change_y < 260 or self.rect.center[1] + self.radius + self.change_y > 433)):
        #     self.change_x = 0
        self.max_min_velocity()
        if 1 > self.change_y > 0:
            self.rect.y += 1
        elif -1 < self.change_y < 0:
            self.rect.y -= 1
        else:
            self.rect.y += round(self.change_y)
        if 1 > self.change_x > 0:
            self.rect.x += 1
        elif -1 < self.change_x < 0:
            self.rect.x -= 1
        else:
            self.rect.x += round(self.change_x)
        self.collision.collisionBall2Wall(self, self.ball_vs_wall_observable)
        self.change_x /= self.prevent
        self.change_y /= self.prevent

        if self.change_x == 0:
            if self.change_y > 0:
                self.degree = -90
            else:
                self.degree = 90
        elif self.change_y == 0:
            if self.change_x > 0:
                self.degree = 0
            else:
                self.degree = 180
        else:
            self.degree = math.atan(math.fabs(self.change_y) / math.fabs(self.change_x)) * 180 / math.pi
            if self.change_x > 0 and self.change_y > 0:
                self.degree = -self.degree
            elif self.change_x > 0 > self.change_y:
                pass
            elif self.change_x < 0 < self.change_y:
                self.degree += 180
            elif self.change_x < 0 and self.change_y < 0:
                self.degree += (90 - self.degree) * 2
        # print(self.degree)
        self.rotate(self.degree)

    def set_velocity(self, vx, vy):
        self.change_x = vx
        self.change_y = vy

    def max_min_velocity(self):
        if self.change_y > Ball.MAX_VELOCITY:
            self.change_y = Ball.MAX_VELOCITY
        if self.change_x > Ball.MAX_VELOCITY:
            self.change_x = Ball.MAX_VELOCITY
        if Ball.BALL_STOP_BOUND > self.change_x > -Ball.BALL_STOP_BOUND and Ball.BALL_STOP_BOUND > self.change_y > -Ball.BALL_STOP_BOUND:
            self.change_x = 0
            self.change_y = 0


class BallShadow(Animation):
    OFFSET_X = -10
    OFFSET_Y = -10

    def __init__(self, manager, ball, frame, speed=1000):
        Animation.__init__(self, manager, frame, speed)
        self.ball = ball

    def update(self):
        Animation.update(self)
        self.set_position_center(self.ball.rect.x + self.ball.rect.width + BallShadow.OFFSET_X,
                                 self.ball.rect.y + self.ball.rect.height + BallShadow.OFFSET_Y)


class GoalScreen(Animation):
    def __init__(self, manager, frame, speed=1000):
        Animation.__init__(self, manager, frame, speed)
        self.rect.x = 0
        self.rect.y = 0


class Button(pygame.sprite.Sprite):
    def __init__(self, frames, position):
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames
        self.position = position
        self.rect = frames[0].get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.image = frames[0]
        self.radius = frames[0].get_rect().width / 2
        self.current_frame = 0

    def update(self, mouse, event_list):
        if self.is_mouse_over(mouse):
            self.image = self.frames[1]
        else:
            self.image = self.frames[0]

    def is_mouse_over(self, mouse):
        distance = math.pow(mouse[0] - self.rect.center[0], 2) + math.pow(mouse[1] - self.rect.center[1], 2)
        return distance <= math.pow(self.radius, 2)


class SlideButton(Button):
    def __init__(self, frames, position):
        Button.__init__(self, frames, position)

    def update(self, mouse, event_list):
        pass

    def toggle_frame(self):
        self.current_frame = (self.current_frame + 1) % 2
        self.image = self.frames[self.current_frame]