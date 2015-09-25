__author__ = 'Hieu'
"""
Implement stuff such as background, score board
"""
import data
from animation import *


class Platform:
    background = pygame.image.load("images/background-v4.jpg")
    background = pygame.transform.scale(background, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    goal_left = pygame.image.load("images/goal-left.png")
    goal_right = pygame.image.load("images/goal-right.png")
    gameover = pygame.image.load("images/gameover-screen.png")
    gamestart = pygame.image.load("images/startscreen.jpg")

    trophy = pygame.image.load("images/trophy.png")

    def __init__(self, scr):
        self.screen = scr
        # gameover setting
        self.gameover_button_list = []
        self.gameover_button_group = pygame.sprite.Group()
        gameover_button_sprite = pygame.image.load("images/buttons.png")
        gameover_mute_button_frames = [gameover_button_sprite.subsurface(
            pygame.Rect(data.gamepverButtonFramesData[0][0], data.gamepverButtonFramesData[0][1],
                        data.gamepverButtonFramesData[0][2],
                        data.gamepverButtonFramesData[0][3])), gameover_button_sprite.subsurface(
            pygame.Rect(data.gamepverButtonFramesData[1][0], data.gamepverButtonFramesData[1][1],
                        data.gamepverButtonFramesData[1][2],
                        data.gamepverButtonFramesData[1][3]))]

        gameover_mute_button = Button(gameover_mute_button_frames, constants.GAMEOVER_BUTTON_POS[0])
        gameover_replay_button_framse = [gameover_button_sprite.subsurface(
            pygame.Rect(data.gamepverButtonFramesData[2][0], data.gamepverButtonFramesData[2][1],
                        data.gamepverButtonFramesData[2][2],
                        data.gamepverButtonFramesData[2][3])), gameover_button_sprite.subsurface(
            pygame.Rect(data.gamepverButtonFramesData[3][0], data.gamepverButtonFramesData[3][1],
                        data.gamepverButtonFramesData[3][2],
                        data.gamepverButtonFramesData[3][3]))]

        gameover_replay_button = Button(gameover_replay_button_framse, constants.GAMEOVER_BUTTON_POS[1])
        gameover_exit_button_framse = [gameover_button_sprite.subsurface(
            pygame.Rect(data.gamepverButtonFramesData[4][0], data.gamepverButtonFramesData[4][1],
                        data.gamepverButtonFramesData[4][2],
                        data.gamepverButtonFramesData[4][3])), gameover_button_sprite.subsurface(
            pygame.Rect(data.gamepverButtonFramesData[5][0], data.gamepverButtonFramesData[5][1],
                        data.gamepverButtonFramesData[5][2],
                        data.gamepverButtonFramesData[5][3]))]

        gameover_exit_button = Button(gameover_exit_button_framse, constants.GAMEOVER_BUTTON_POS[2])
        self.gameover_button_list.append(gameover_mute_button)
        self.gameover_button_list.append(gameover_replay_button)
        self.gameover_button_list.append(gameover_exit_button)
        for button in self.gameover_button_list:
            self.gameover_button_group.add(button)

        # gamestart setting
        self.gamestart_button_list = []
        self.gamestart_button_group = pygame.sprite.Group()
        gamestart_button_sprite = pygame.image.load("images/start-buttons.png")

        gamestart_exit_button_frames = [gamestart_button_sprite.subsurface(
            pygame.Rect(data.gamestartButtonFramesData[0][0], data.gamestartButtonFramesData[0][1],
                        data.gamestartButtonFramesData[0][2],
                        data.gamestartButtonFramesData[0][3])), gamestart_button_sprite.subsurface(
            pygame.Rect(data.gamestartButtonFramesData[1][0], data.gamestartButtonFramesData[1][1],
                        data.gamestartButtonFramesData[1][2],
                        data.gamestartButtonFramesData[1][3]))]

        gamestart_exit_button = Button(gamestart_exit_button_frames, constants.START_BUTTON_POS[0])

        gamestart_play_button_frames = [gamestart_button_sprite.subsurface(
            pygame.Rect(data.gamestartButtonFramesData[2][0], data.gamestartButtonFramesData[2][1],
                        data.gamestartButtonFramesData[2][2],
                        data.gamestartButtonFramesData[2][3])), gamestart_button_sprite.subsurface(
            pygame.Rect(data.gamestartButtonFramesData[3][0], data.gamestartButtonFramesData[3][1],
                        data.gamestartButtonFramesData[3][2],
                        data.gamestartButtonFramesData[3][3]))]

        gamestart_play_button = Button(gamestart_play_button_frames, constants.START_BUTTON_POS[1])

        gamestart_mute_button_frames = [gamestart_button_sprite.subsurface(
            pygame.Rect(data.gamestartButtonFramesData[4][0], data.gamestartButtonFramesData[4][1],
                        data.gamestartButtonFramesData[4][2],
                        data.gamestartButtonFramesData[4][3])), gamestart_button_sprite.subsurface(
            pygame.Rect(data.gamestartButtonFramesData[5][0], data.gamestartButtonFramesData[5][1],
                        data.gamestartButtonFramesData[5][2],
                        data.gamestartButtonFramesData[5][3]))]

        self.gamestart_mute_button = SlideButton(gamestart_mute_button_frames, constants.START_BUTTON_POS[2])
        self.gamestart_button_list.append(gamestart_exit_button)
        self.gamestart_button_list.append(gamestart_play_button)
        self.gamestart_button_list.append(self.gamestart_mute_button)
        for button in self.gamestart_button_list:
            self.gamestart_button_group.add(button)
        # Text inti
        self.font_obj = pygame.font.Font("fonts/Digital Dismay.otf", 70)


    def draw(self):
        self.screen.fill(constants.BlUE)
        self.screen.blit(self.background, (0, 0))


    def update(self):
        pass


    def draw_goal(self):
        self.screen.blit(self.goal_left, constants.GOAL_LEFT_POS)
        self.screen.blit(self.goal_right, constants.GOAL_RIGHT_POS)


    def gameover_screen(self, mouse, event_list, scores):
        self.draw()
        self.draw_goal()
        self.screen.blit(self.gameover, (0, 0))



        # self.screen.blit(self.button_frames[0], constants.BUTTON_POS[0])
        self.gameover_button_group.draw(self.screen)
        self.gameover_button_group.update(mouse, event_list)
        text_surf_obj = self.font_obj.render(
            Scoreboard.score_format(scores[0]) + ":" + Scoreboard.score_format(scores[1]), True, constants.SCORE_COLOR,
            None)
        text_rect_obj = text_surf_obj.get_rect()
        text_rect_obj.center = constants.SCORE_POS
        self.screen.blit(text_surf_obj, text_rect_obj)
        if (scores[0] > scores[1]):
            self.screen.blit(self.trophy, constants.TROPHY_POS[0])
        else:
            self.screen.blit(self.trophy, constants.TROPHY_POS[1])
            # def gameover_screen_update(self, mouse_pos):

    def gamestart_screen(self, mouse, event_list):
        self.screen.blit(self.gamestart, (0, 0))
        self.gamestart_button_group.draw(self.screen)
        self.gamestart_button_group.update(mouse, event_list)

class Scoreboard():
    def __init__(self, screen):
        self.plsy_time_start = pygame.time.get_ticks()
        self.score_time_list = [[], []]
        self.scores = [0, 0]
        self.screen = screen
        self.font_obj = pygame.font.Font("fonts/Digital Dismay.otf", 65)
        self.text_surf_obj = self.font_obj.render(
            Scoreboard.score_format(self.scores[0]) + ":" + Scoreboard.score_format(self.scores[1]), True,
            constants.WHITE, None)
        self.text_rect_obj = self.text_surf_obj.get_rect()
        self.text_rect_obj.center = 500, 50

    def update(self):
        self.text_surf_obj = self.font_obj.render(
            Scoreboard.score_format(self.scores[0]) + ":" + Scoreboard.score_format(self.scores[1]), True,
            constants.WHITE, None)
        self.screen.blit(self.text_surf_obj, self.text_rect_obj)

    @staticmethod
    def score_format(num):
        if 0 <= num < 10:
            return "0" + str(num)
        else:
            return str(num)

    def set_score(self, index, score):
        self.scores[index] = score

    def inc_score(self, index):
        self.scores[index] += 1
        self.score_time_list[index].append((pygame.time.get_ticks() - self.plsy_time_start) / 1000)
        print(self.score_time_list)

    def dec_score(self, index):
        self.scores[index] -= 1

    def reset_score(self):
        self.scores = [0, 0]
