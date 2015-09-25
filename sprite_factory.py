__author__ = 'Hieu'
"""
This module is used to pull individual sprites from sprite sheets.
"""

import pygame


class SpriteFactory(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
        return self.sprite_sheet.subsurface(x, y, width, height).convert_alpha()

    @staticmethod
    def append_frame(sprite, frames, x, y, width, height):
        image = sprite.get_image(x, y, width, height)
        frames.append(image)

    @staticmethod
    def generate_frames(sprite, frame_data):
        frames = []
        for item in frame_data:
            SpriteFactory.append_frame(sprite, frames, item[0], item[1], item[2], item[3])
        return frames
