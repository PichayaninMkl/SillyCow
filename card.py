import arcade
import os
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Card(arcade.Sprite):
    """ Card class """

    def __init__(self, image, scale):
        """ Set up the Card """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

    def update(self):
        # Rotate the ship
        self.angle += self.change_angle

    def set_pos(self, x, y):
        # print(self.center_x, self.center_y)
        self.center_y = (SCREEN_HEIGHT / 2)
        self.center_x = x