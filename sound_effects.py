import pygame


class SoundEffects:
    def __init__(self):
        self.ball_vs_wall = pygame.mixer.Sound("sounds/ball-vs-wall.wav")
        self.end_game = pygame.mixer.Sound("sounds/end-game.wav")
        self.goal = pygame.mixer.Sound("sounds/goal.wav")
        self.player_kick_ball = pygame.mixer.Sound("sounds/player-kick-ball.wav")
        self.player_vs_player = pygame.mixer.Sound("sounds/player-vs-player.wav")
        self.start_game = pygame.mixer.Sound("sounds/start-game.wav")
        self.start_screen = pygame.mixer.Sound("sounds/start_screen.wav")
        self.stadium_sound = pygame.mixer.music.load('sounds/fans-cheering.wav')
        self.mouseover_sound = pygame.mixer.Sound("sounds/mouse_over.wav")

        self.is_muted = False

    def play_mouseover(self):
        self.mouseover_sound.play()

    def play_ball_vs_wall(self):
        if self.is_muted == False:
            self.ball_vs_wall.play()

    def play_end_game(self):
        self.end_game.play()

    def play_goal(self):
        self.goal.play()

    def play_player_kick_ball(self):
        if self.is_muted == False:
            self.player_kick_ball.play()

    def play_player_vs_player(self):
        self.player_vs_player.play()

    def play_start_game(self):
        self.start_game.play()

    def play_start_screen(self):
        self.start_screen.play(-1)

    def stop_start_screen(self):
        self.start_screen.stop()

    def set_mute(self):
        self.ball_vs_wall.set_volume(0)
        self.end_game.set_volume(0)
        self.goal.set_volume(0)
        self.player_kick_ball.set_volume(0)
        self.player_vs_player.set_volume(0)
        self.start_game.set_volume(0)
        self.start_screen.set_volume(0)
        pygame.mixer.music.set_volume(0)
        self.is_muted = True

    def set_unmute(self):
        self.ball_vs_wall.set_volume(1)
        self.end_game.set_volume(1)
        self.goal.set_volume(1)
        self.player_kick_ball.set_volume(1)
        self.player_vs_player.set_volume(1)
        self.start_game.set_volume(1)
        self.start_screen.set_volume(1)
        pygame.mixer.music.set_volume(1)
        self.is_muted = False
