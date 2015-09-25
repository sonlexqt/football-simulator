__author__ = 'Hieu'

from sprite_factory import SpriteFactory
from user import *
from platform import *
from sound_effects import SoundEffects
from pygame import mouse
from collision import  Collision


class GameManager:
    clock = pygame.time.Clock()

    def __init__(self):
        self.number_of_user = 0
        self.userList = []
        self.player_list = []
        self.screen = None
        self.sfx = SoundEffects()
        self.display_init()
        self.sprite_group = pygame.sprite.Group()
        self.focus_effect_group = pygame.sprite.Group()
        self.goal_effect_group = pygame.sprite.Group()
        self.ball = self.ball_init(self.sfx)
        self.user_init(self.ball, self.sfx)
        self.platform = None
        self.platform_init()
        self.done = False
        self.focus_effect_blue = None
        self.focus_effect_red = None
        self.focus_effect_list = []
        self.focus_effect_init()
        self.collision = Collision()
        self.scoreboard = Scoreboard(self.screen)
        self.ball_reset_delay = 2000
        self.goal_effect_init()
        self.max_score = 3

    def display_init(self):
        size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Hello world")

    def user_init(self, ball, sfx):
        player_sprite = SpriteFactory("images/player.png")
        user1_players_initial_positions = constants.USER1_PLAYERS_INITIAL_POS
        user2_players_initial_positions = constants.USER2_PLAYERS_INITIAL_POS
        user1 = User(self.sprite_group, player_sprite, data.playerBlueFramesData, user1_players_initial_positions, ball, sfx)
        self.add_user(user1)
        self.add_player(user1)
        user2 = User(self.sprite_group, player_sprite, data.playerRedFramesData, user2_players_initial_positions, ball, sfx)
        self.add_user(user2)
        self.add_player(user2)

    def ball_init(self, sfx):
        ball_sprite = SpriteFactory("images/ball-small.png")
        ball_frames = SpriteFactory.generate_frames(ball_sprite, data.ballFramesData)
        ball = Ball(self.sprite_group, (constants.BALL_INIT_POS[0], constants.BALL_INIT_POS[1]), ball_frames, sfx, speed=100)
        ball.play(Animation.INFINITE)

        ball_shadow_sprite = SpriteFactory("images/ball-shadow.png")
        ball_shadow_frames = SpriteFactory.generate_frames(ball_shadow_sprite, data.ballShadowFramesData)
        ball_shadow = BallShadow(self.focus_effect_group, ball, ball_shadow_frames, speed=1000)
        ball_shadow.play(Animation.INFINITE)
        return ball

    def platform_init(self):
        self.platform = Platform(self.screen)

    def focus_effect_init(self):
        focus_effect_sprite_red = SpriteFactory("images/hover-red.png")
        focus_effect_frames_red = SpriteFactory.generate_frames(focus_effect_sprite_red, data.hoverEffectFramesData)
        focus_effect_sprite_blue = SpriteFactory("images/hover-blue.png")
        focus_effect_frames_blue = SpriteFactory.generate_frames(focus_effect_sprite_blue, data.hoverEffectFramesData)
        focus_effect_blue = FocusEffect(self.focus_effect_group,
                                        self.userList[0].players_list[self.userList[0].current_selected_player],
                                        focus_effect_frames_blue, speed=1000)
        self.focus_effect_list.append(focus_effect_blue)
        self.focus_effect_list[0].play(Animation.INFINITE)
        focus_effect_red = FocusEffect(self.focus_effect_group,
                                       self.userList[1].players_list[self.userList[1].current_selected_player],
                                       focus_effect_frames_red, speed=1000)
        self.focus_effect_list.append(focus_effect_red)
        self.focus_effect_list[1].play(Animation.INFINITE)

    def goal_effect_init(self):
        goal_effect_sprite = SpriteFactory("images/goal-screen.png")
        goal_effect_frames = SpriteFactory.generate_frames(goal_effect_sprite, data.goalEffectFramesData)
        self.goal_effect = GoalScreen(self.goal_effect_group, goal_effect_frames)

        # self.userList[0].players_list[1].rect.x = 200
        # self.userList[1].players_list[1].rect.y = 700

    # @param user: type User
    def add_user(self, user):
        self.userList.append(user)

    def add_player(self, user):
        for x in range(0, user.num_of_players):
            self.player_list.append(user.players_list[x])

    def is_game_over(self):
        user1_score = self.scoreboard.scores[0]
        user2_score = self.scoreboard.scores[1]
        if user1_score > self.max_score / 2 and user1_score > user2_score:  # user1 win
            return True
        elif user2_score > self.max_score / 2 and user2_score > user1_score:  # user2 win
            return True
        else:
            return False

    def gameover_screen(self):
        exitLoop = False
        while not exitLoop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitLoop = True
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(0, len(self.platform.gameover_button_list), 1):
                        if self.platform.gameover_button_list[i].is_mouse_over(mouse.get_pos()):
                            if i == constants.GAMEOVER_BUTTON_TYPE["mute"]:
                                self.sfx.play_mouseover()
                                if self.sfx.is_muted == True:
                                    self.sfx.set_unmute()
                                else:
                                    self.sfx.set_mute()
                            elif i == constants.GAMEOVER_BUTTON_TYPE["replay"]:
                                self.sfx.play_mouseover()
                                exitLoop = True
                                self.scoreboard.reset_score()
                                self.start(False)
                            elif i == constants.GAMEOVER_BUTTON_TYPE["exit"]:
                                self.sfx.play_mouseover()
                                exitLoop = True
                                self.done = True
            self.platform.gameover_screen(mouse.get_pos(), pygame.event.get(), self.scoreboard.scores)
            pygame.display.update()
            GameManager.clock.tick(constants.FPS)


    def start_screen(self):
        exitLoop = False
        self.sfx.play_start_screen()
        while not exitLoop:
            # for i in range(0, len(self.platform.gamestart_button_list), 1):
            #      if self.platform.gamestart_button_list[i].is_mouse_over(mouse.get_pos()) and i is not constants.GAMESTART_BUTTON_TYPE["mute"]:
            #              self.sfx.play_mouseover()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(0, len(self.platform.gamestart_button_list), 1):
                        if self.platform.gamestart_button_list[i].is_mouse_over(mouse.get_pos()):
                            if i == constants.GAMESTART_BUTTON_TYPE["mute"]:
                                self.sfx.play_mouseover()
                                self.platform.gamestart_mute_button.toggle_frame()
                                if self.sfx.is_muted == True:
                                    self.sfx.set_unmute()
                                else:
                                    self.sfx.set_mute()
                            elif i == constants.GAMESTART_BUTTON_TYPE["play"]:
                                self.sfx.play_mouseover()
                                exitLoop = True
                                self.sfx.stop_start_screen()
                                self.scoreboard.reset_score()
                                self.start(False)
                            elif i == constants.GAMESTART_BUTTON_TYPE["exit"]:
                                self.sfx.play_mouseover()
                                exitLoop = True
                                self.done = True
            self.platform.gamestart_screen(mouse.get_pos(), pygame.event.get())
            pygame.display.update()
            GameManager.clock.tick(constants.FPS)

    def start(self, is_show_start_screen):
        if is_show_start_screen:
            self.start_screen()
        pygame.mixer.music.play(-1)  # Play the fans cheering music
        self.sfx.play_start_game()
        last_time_updated = pygame.time.get_ticks()
        is_resetting_game = False
        for user in self.userList:
            user.reset_players_position()
        pygame.key.set_repeat(1, 20)
        # Main Program Loop
        while not self.done:
            # Move all players in a team at the same time
            keys = pygame.key.get_pressed()
            # Move all user1's players
            if keys[pygame.K_LSHIFT]:
                if keys[pygame.K_d]:
                    for player in self.userList[0].players_list:
                        player.go_right()
                elif keys[pygame.K_a]:
                    for player in self.userList[0].players_list:
                        player.go_left()
                elif keys[pygame.K_w]:
                    for player in self.userList[0].players_list:
                        player.go_up()
                elif keys[pygame.K_s]:
                    for player in self.userList[0].players_list:
                        player.go_down()
            # Move all user2's players
            if keys[pygame.K_RCTRL]:
                if keys[pygame.K_RIGHT]:
                    for player in self.userList[1].players_list:
                        player.go_right()
                elif keys[pygame.K_LEFT]:
                    for player in self.userList[1].players_list:
                        player.go_left()
                elif keys[pygame.K_UP]:
                    for player in self.userList[1].players_list:
                        player.go_up()
                elif keys[pygame.K_DOWN]:
                    for player in self.userList[1].players_list:
                        player.go_down()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True

                    # User1 input handlers
                    for i in range(0, len(data.controllerSetting), 1):
                        user_setting = data.controllerSetting[i]
                        user = self.userList[i]
                        # if event.key == user_setting['next'] and not self.automatic_choose:
                        #     user.players_list[user.current_selected_player].stop()
                        #     user.current_selected_player = (user.current_selected_player + 1) % user.num_of_players
                        #     user.focused_player_index = user.current_selected_player
                        #     self.focus_effect_list[i].set_player(user.players_list[user.current_selected_player])
                        if event.key == user_setting['left']:
                            user.players_list[user.current_selected_player].go_left()
                        if event.key == user_setting['right']:
                            user.players_list[user.current_selected_player].go_right()
                        if event.key == user_setting['up']:
                            user.players_list[user.current_selected_player].go_up()
                        if event.key == user_setting['down']:
                            user.players_list[user.current_selected_player].go_down()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_F5:
                        # Hot reset the game
                        self.scoreboard.reset_score()
                        self.ball.goal = False
                        self.ball.is_ball_going_in = False
                        self.ball.change_x = 0
                        self.ball.change_y = 0
                        self.ball.set_position_center(constants.BALL_INIT_POS[0], constants.BALL_INIT_POS[1])
                        self.ball.is_ball_hit_wall = False
                        self.start(False)
                    if event.key == pygame.K_m:
                        if self.sfx.is_muted == True:
                            self.sfx.set_unmute()
                        else:
                            self.sfx.set_mute()
                    for i in range(0, len(data.controllerSetting), 1):
                        user_setting = data.controllerSetting[i]
                        user = self.userList[i]
                        if event.key == user_setting['next'] or event.key == user_setting['left'] or event.key == \
                                user_setting['right'] or event.key == user_setting['up'] or event.key == user_setting[
                            'down']:
                            user.players_list[user.current_selected_player].stop()
                            user.isInControl = False

            # TODO a goal scored !
            if self.ball.goal:
                self.goal_effect.play(2)
                if is_resetting_game == False:
                    self.sfx.play_goal()
                now = pygame.time.get_ticks()
                if is_resetting_game == True and (now - last_time_updated) >= self.ball_reset_delay:
                    # Update score
                    self.scoreboard.inc_score(data.winner)
                    self.ball.goal = False
                    self.ball.is_ball_going_in = False
                    self.ball.change_x = 0
                    self.ball.change_y = 0
                    self.ball.set_position_center(constants.BALL_INIT_POS[0], constants.BALL_INIT_POS[1])
                    self.ball.is_ball_hit_wall = False
                    for user in self.userList:
                        user.reset_players_position()
                    if self.is_game_over():
                        print("GAME OVER")
                        self.sfx.play_goal()
                        self.sfx.play_end_game()
                        self.gameover_screen()
                    else:
                        self.sfx.play_start_game()
                        is_resetting_game = False
                        continue
                is_resetting_game = True

            if is_resetting_game == False:
                last_time_updated = pygame.time.get_ticks()

            # Update the players
            self.focus_effect_group.update()
            # test
            for x in range(0, len(self.player_list)):
                for y in range(x + 1, len(self.player_list)):
                    self.collision.collisionPlayer2Player(self.player_list[x], self.player_list[y], self.sfx)
                            
            # Update the player
            self.focus_effect_group.update()
            self.sprite_group.update()
            self.platform.update()
            self.goal_effect_group.update()
            for i in range(0, len(self.userList), 1):
                self.userList[i].update(self.focus_effect_list[i])
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            self.platform.draw()
            self.focus_effect_group.draw(self.screen)
            self.sprite_group.draw(self.screen)
            self.platform.draw_goal()
            self.scoreboard.update()
            self.goal_effect_group.draw(self.screen)
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            # rect = self.user_init(self.ball_init()).players_list[0].rect.center
            # pygame.draw.circle(self.screen, (255,255,255), (rect[0]+2,rect[1]), 37)
            # Limit to 60 frames per second
            GameManager.clock.tick(constants.FPS)

            # Go ahead and update the screen with what we've drawn
            pygame.display.flip()

        # Be IDLE friendly. If you forget this line, the program will 'hange'
        # on exit.
        pygame.quit()


