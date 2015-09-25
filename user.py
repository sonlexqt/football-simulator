from player import Player
import math
import random
from constants import *


class User:
    def __init__(self, active_sprite_list, player_sprite, player_frame_data, players_initial_positions, ball, sfx):
        self.default_pos = players_initial_positions
        self.ball = ball
        self.players_positions = players_initial_positions
        self.num_of_players = len(players_initial_positions)
        self.current_selected_player = 0
        self.players_list = []
        self.focused_player_index = 0
        self.players_initial_positions = players_initial_positions
        self.player_index = 0
        for player_position in players_initial_positions:
            self.player_index += 1
            self.players_list.append(Player(active_sprite_list, player_sprite, player_frame_data, player_position, ball, sfx))

    def set_focused_player_index(self, index):
        normal_index = index % len(self.players_list)
        self.focused_player_index = normal_index

    def get_focused_player_index(self):
        return self.focused_player_index

    def update(self, focus_effect):
        focused_player = self.get_closest_player()
        self.set_focused_player_index(focused_player)
        focus_effect.set_player(self.players_list[self.focused_player_index])
        if self.focused_player_index is not self.current_selected_player:
            self.players_list[self.current_selected_player].stop()
            self.current_selected_player = self.focused_player_index
            self.players_list[self.current_selected_player].stop()
        for i in range(0, len(self.players_list), 1):
            if i is not self.focused_player_index and not self.is_in_default_pos(self.default_pos[i], self.players_list[i].rect):
                self.comeback(self.default_pos[i], self.players_list[i])

        # for i in range(0, len(self.players_list), 1):
        #     # if this player is not in control
        #     if i is not self.current_selected_player:
        #         # if this player has collision
        #         if len(self.players_list[i].collision_players) is not 0:
        #             print("hoooooray")
        #             this_player = self.players_list[i]
        #             this_player.direction = self.get_direction_to_get_out_of_collision(this_player)

    def get_direction_to_get_out_of_collision(self, player):
        direct_x = 0
        direct_y = 0
        for col_player in player.collision_players:
            direct_x += player.change_x - col_player.change_x
            direct_y += player.change_y - col_player.change_y
        return direct_x, direct_y

    def get_closest_player(self):
        player_index = None
        closest_distance = float("inf")
        for i in range(0, len(self.players_list), 1):
            distance = math.pow(self.ball.rect.center[0] - self.players_list[i].rect.center[0], 2) + math.pow(
                self.ball.rect.center[1] - self.players_list[i].rect.center[1], 2)
            if distance < closest_distance:
                closest_distance = distance
                player_index = i
        return player_index

    def reset_players_position(self):
        for i in range(len(self.players_list)):
            self.players_list[i].rect.x = self.players_initial_positions[i][0]
            self.players_list[i].rect.y = self.players_initial_positions[i][1]
            self.players_list[i].change_x, self.players_list[i].change_y = 0, 0

    def comeback(self, des, player):
        vx = des[0] - player.rect.x
        vy = des[1] - player.rect.y
        max_vec = max(math.fabs(vx), math.fabs(vy))
        if max_vec == 0:
            player.change_x = 0
            player.change_y = 0
        else:
            # rand = random.randint(1, 3)
            player.change_x = (vx / max_vec) + player.direction[0] * 2
            player.change_y = (vy / max_vec) + player.direction[1] * 2
        if player.direction[0] > 0:
            player.direction[0] -= 0.05
        else:
            player.direction[0] += 0.05
        if player.direction[1] > 0:
            player.direction[1] -= 0.05
        else:
            player.direction[1] += 0.05


    def is_in_default_pos(self, point1, point2):
        return math.fabs(point1[0] - point2[0]) <= 5 and math.fabs(point1[1] - point2[1]) <= 5

    def reset_user(self):
        for player in self.players_list:
            player.change_x = 0
            player.change_y = 0

