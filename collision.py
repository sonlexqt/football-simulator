__author__ = 'Huy'
import pygame
import math
import constants
import data

class Collision:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time = [0, 0, 0, 0, 0, 0]
        self.interval = 100

    def collisionBall2Wall(self, obj, ball_vs_wall_observable):
        self.time[2] = self.clock.tick(constants.FPS)
        if ((obj.rect.center[1] + obj.radius + obj.change_y >= (constants.PLAY_SPACE_RECT[1] + constants.PLAY_SPACE_RECT[3]))\
                    or (obj.rect.center[1] - obj.radius + obj.change_y <= constants.PLAY_SPACE_RECT[1])):
            obj.change_y = -obj.change_y
            obj.is_ball_hit_wall = True
            ball_vs_wall_observable.update_observers()
        if ((obj.rect.center[0] - obj.radius <= constants.PLAY_SPACE_RECT[0]) \
                      or (obj.rect.center[0] + obj.radius >= (constants.PLAY_SPACE_RECT[0] + constants.PLAY_SPACE_RECT[2]))):
            if (obj.rect.center[1] - obj.radius >= 260 and obj.rect.center[1] + obj.radius <= 435):
                if (obj.rect.center[0] - obj.radius <= constants.PLAY_SPACE_RECT[0] and obj.change_x < 0) or \
                        (obj.rect.center[0] + obj.radius >= (constants.PLAY_SPACE_RECT[0] + constants.PLAY_SPACE_RECT[2]) and obj.change_x > 0):
                    obj.is_ball_going_in = True
                else:
                    obj.is_ball_going_in = False
            elif (obj.is_ball_going_in == False):
                obj.change_x = -obj.change_x
                obj.is_ball_hit_wall = True
                ball_vs_wall_observable.update_observers()
        if obj.is_ball_going_in == True:
            if ((260 <= obj.rect.center[1] - obj.radius < 265) or (435 >= obj.rect.center[1] + obj.radius > 430)):
                if (obj.change_y > 0 and 260 <= obj.rect.center[1] - obj.radius < 265) or (obj.change_y < 0 and 435 >= obj.rect.center[1] + obj.radius > 430):
                    pass
                else:
                    obj.change_y = -obj.change_y
            if obj.rect.center[0] - obj.radius <= 33:
                obj.change_x = 0
                obj.change_y = 0
                obj.goal = True
                data.winner = 1

            elif obj.rect.center[0] + obj.radius >= 966:
                obj.change_x = 0
                obj.change_y = 0
                obj.goal = True
                data.winner = 0

            elif obj.change_y == 0 and obj.change_x == 0:
                if obj.rect.center[0] > ( constants.PLAY_SPACE_RECT[0] + constants.PLAY_SPACE_RECT[2] ) / 2:
                    data.winner = 0
                else:
                    data.winner = 1
        else:
            obj.is_ball_hit_wall = False

    def collisionPlayer2Wall(self, obj):
        if ((obj.rect.center[1] + obj.radius + obj.change_y >= (constants.SCREEN_HEIGHT))\
                    or (obj.rect.center[1] - obj.radius + obj.change_y <= 10)):
            obj.change_x = 0
            obj.change_y = 0
        elif ((obj.rect.center[0] - obj.radius + obj.change_x <= constants.PLAY_SPACE_RECT[0]) \
                      or (obj.rect.center[0] + obj.radius + obj.change_x >= (constants.PLAY_SPACE_RECT[0] + constants.PLAY_SPACE_RECT[2]))):
            obj.change_x = 0
            obj.change_y = 0

    def collisionPlayer2Ball(self, obj1, obj2, player_vs_ball_observable):
        self.time[0] += self.clock.tick(constants.FPS)
        distance = math.sqrt(((obj1.rect.center[0] + 2 - obj2.rect.center[0]) * (obj1.rect.center[0] + 2 - obj2.rect.center[0])) + ((obj1.rect.center[1] - obj2.rect.center[1]) * (obj1.rect.center[1] - obj2.rect.center[1])))
        if ((distance < obj1.radius + obj2.radius) and ((self.time[0] - self.time[1] > self.interval) or self.time[1] == 0)):
            player_vs_ball_observable.update_observers()
            point = (((obj1.rect.center[0] * obj2.radius) + (obj2.rect.center[0] * obj1.radius)) / (obj1.radius + obj2.radius),\
                     ((obj1.rect.center[1] * obj2.radius) + (obj2.rect.center[1] * obj1.radius)) / (obj1.radius + obj2.radius))
            self.time[1] = self.time[0]
            v1 = (obj2.change_x * (obj2.m - obj1.m) + (2 * obj1.m * obj1.change_x)) / (obj1.m + obj2.m)
            v2 = (obj2.change_y * (obj2.m - obj1.m) + (2 * obj1.m * obj1.change_y)) / (obj1.m + obj2.m)
            if (v1 == 0.0):
                newV1 = obj1.rect.center[0] + 2 - obj2.rect.center[0]
                newV2 = obj1.rect.center[1] - obj2.rect.center[1]
                newV = newV1 / newV2
                v1 = v2 * newV
            if (v2 == 0.0):
                newV1 = obj1.rect.center[0] + 2 - obj2.rect.center[0]
                newV2 = obj1.rect.center[1] - obj2.rect.center[1]
                newV = newV2 / newV1
                v2 = v1 * newV
            obj2.change_x = v1
            obj2.change_y = v2

            self.checkDirection(obj1, obj2)
            if (distance < obj1.radius + obj2.radius - 15):
                obj2.change_x = -(obj1.rect.center[1] - obj2.rect.center[1])
                obj2.change_y = obj1.rect.center[0] + 2 - obj2.rect.center[0]

    @staticmethod
    def collisionPlayer2Player(obj1, obj2, sfx):
        distance = math.sqrt(((obj1.rect.center[0] + obj1.change_x - obj2.rect.center[0] - obj2.change_x) * \
                              (obj1.rect.center[0] + obj1.change_x - obj2.rect.center[0] - obj2.change_x)) + \
                             ((obj1.rect.center[1] + obj1.change_y - obj2.rect.center[1] - obj2.change_y) * \
                              (obj1.rect.center[1] + obj1.change_y - obj2.rect.center[1] - obj2.change_y)))
        if (distance <= obj1.radius + obj2.radius):
            obj1.change_x = 0
            obj1.change_y = 0
            obj2.change_x = 0
            obj2.change_y = 0
            if sfx is not None:
                sfx.play_player_vs_player()
            obj1.direction[0] += obj1.rect.center[0] - obj2.rect.center[0]
            obj1.direction[1] += obj1.rect.center[1] - obj2.rect.center[1]
            # normalize
            obj1_direction_length = math.sqrt(math.pow(obj1.direction[0], 2) + math.pow(obj1.direction[1], 2))
            obj1.direction[0] /= obj1_direction_length
            obj1.direction[1] /= obj1_direction_length

            obj2.direction[0] += obj2.rect.center[0] - obj1.rect.center[0]
            obj2.direction[1] += obj2.rect.center[1] - obj1.rect.center[1]
            # normalize
            obj2_direction_length = math.sqrt(math.pow(obj2.direction[0], 2) + math.pow(obj2.direction[1], 2))
            obj2.direction[0] /= obj2_direction_length
            obj2.direction[1] /= obj2_direction_length

    @staticmethod
    def checkDirection(obj1, obj2):
        point = ((((obj1.rect.center[0] + 2) * obj2.radius) + (obj2.rect.center[0] * obj1.radius)) / (obj1.radius + obj2.radius),\
                     ((obj1.rect.center[1] * obj2.radius) + (obj2.rect.center[1] * obj1.radius)) / (obj1.radius + obj2.radius))
        if (point[0] < constants.PLAY_SPACE_RECT[0] + 50 or point[0] > constants.PLAY_SPACE_RECT[0] + constants.PLAY_SPACE_RECT[2] - 50):
            if (point[1] >= obj1.rect.center[1]):
                obj2.change_y = 5
            else:
                obj2.change_y = 5
        elif (point[1] < constants.PLAY_SPACE_RECT[1] + 50 or point[1] > constants.PLAY_SPACE_RECT[1] + constants.PLAY_SPACE_RECT[3] - 50):
            if (point[0] >= obj1.rect.center[0]):
                obj2.change_x = 5
            else:
                obj2.change_x = 5