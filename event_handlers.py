from observable import Observable
from observer import Observer


class BallVsWallObserver(Observer):
    def __init__(self, sfx):
        self.sfx = sfx

    def update(self, *args, **kwargs):
        self.sfx.play_ball_vs_wall()


class BallVsWallObservable(Observable):
    pass


class PlayerVsBallObserver(Observer):
    def __init__(self, sfx):
        self.sfx = sfx

    def update(self, *args, **kwargs):
        self.sfx.play_player_kick_ball()


class PlayerVsBallObservable(Observable):
    pass

