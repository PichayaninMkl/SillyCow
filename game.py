import arcade
import os
import math
from card import Card

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Silly Cow"

ANGLE = 120

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.card_list = arcade.SpriteList()

        # Set up the Card info
        self.cow_center = None
        self.horse_center = None
        self.pig_center = None
        self.sheep_center = None
        self.cow = None
        self.horse = None
        self.pig = None
        self.sheep = None

        # set position all card
        self.cow_position = 0
        self.horse_position = 0
        self.pig_position = 0
        self.sheep_position = 0
        self.bot_button_position = 0

        # card select
        self.card_select = None

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup_cow(self):
        """ Set up the game and initialize the variables. """
        self.cow_center = Card("card/cow_center.png", SPRITE_SCALING)
        self.cow_center.center_x = (SCREEN_WIDTH / 2)-150
        self.cow_center.center_y = SCREEN_HEIGHT / 2
        self.card_list.append(self.cow_center)

        self.cow = Card("card/cow.png", SPRITE_SCALING)
        self.cow.center_x = SCREEN_WIDTH * 0.45

    def setup_horse(self):
        self.horse_center = Card("card/horse_center.png", SPRITE_SCALING)
        self.horse_center.center_x = (SCREEN_WIDTH / 2)-50
        self.horse_center.center_y = SCREEN_HEIGHT / 2
        self.card_list.append(self.horse_center)

        self.horse = Card("card/horse.png", SPRITE_SCALING)
        self.horse.center_x = SCREEN_WIDTH * 0.5

    def setup_pig(self):
        self.pig_center = Card("card/pig_center.png", SPRITE_SCALING)
        self.pig_center.center_x = (SCREEN_WIDTH / 2)+50
        self.pig_center.center_y = SCREEN_HEIGHT / 2
        self.card_list.append(self.pig_center)

        self.pig = Card("card/pig.png", SPRITE_SCALING)
        self.pig.center_x = SCREEN_WIDTH * 0.55

    def setup_sheep(self):
        self.sheep_center = Card("card/sheep_center.png", SPRITE_SCALING)
        self.sheep_center.center_x = (SCREEN_WIDTH / 2)+150
        self.sheep_center.center_y = SCREEN_HEIGHT / 2
        self.card_list.append(self.sheep_center)

        self.sheep = Card("card/sheep.png", SPRITE_SCALING)
        self.sheep.center_x = SCREEN_WIDTH * 0.6

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all card at center.
        self.card_list.draw()
        self.cow.draw()
        self.horse.draw()
        self.pig.draw()
        self.sheep.draw()
        # arcade.draw_text("Start bot",
        #                  (SCREEN_WIDTH / 7),(SCREEN_HEIGHT / 7), arcade.color.WHITE, 24, anchor_x="left", anchor_y="top")

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        # self.cow_list.update()
        pass

    # def on_mouse_press(self,)    
         
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Rotate left/right
        if key == arcade.key.C:
            # print(self.card_select)
            # print(self.cow_position)
            self.card_select = "C"
        elif key == arcade.key.H:
            # print(self.card_select)
            self.card_select = "H"
        elif key == arcade.key.P:
            # print(self.card_select)
            self.card_select = "P"
        elif key == arcade.key.S:
            # print(self.card_select)
            self.card_select = "S"
        elif key == arcade.key.LEFT and self.card_select == "C" and self.cow_position == 0:
            self.cow_center.remove_from_sprite_lists()
            self.cow.set_pos(self.cow.center_x, self.cow.center_y)
            self.cow_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "C" and self.cow_position != 0:
            self.cow.change_angle = ANGLE
            self.cow.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "C" and self.cow_position == 0:
            self.cow_center.remove_from_sprite_lists()
            self.cow.set_pos(self.cow.center_x, self.cow.center_y)
            self.cow_position = 1
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "C" and self.cow_position != 0:
            self.cow.change_angle = -ANGLE
            self.cow.update()
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "H" and self.horse_position == 0:
            self.horse_center.remove_from_sprite_lists()
            self.horse.set_pos(self.horse.center_x, self.horse.center_y)
            self.horse_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "H" and self.horse_position != 0:
            self.horse.change_angle = ANGLE
            self.horse.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "H" and self.horse_position == 0:
            self.horse_center.remove_from_sprite_lists()
            self.horse.set_pos(self.horse.center_x, self.horse.center_y)
            self.horse_position = 1
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "H" and self.horse_position != 0:
            self.horse.change_angle = -ANGLE
            self.horse.update()
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "P" and self.pig_position == 0:
            self.pig_center.remove_from_sprite_lists()
            self.pig.set_pos(self.pig.center_x, self.pig.center_y)
            self.pig_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "P" and self.pig_position != 0:
            self.pig.change_angle = ANGLE
            self.pig.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "P" and self.pig_position == 0:
            self.pig_center.remove_from_sprite_lists()
            self.pig.set_pos(self.pig.center_x, self.pig.center_y)
            self.pig_position = 1
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "P" and self.pig_position != 0:
            self.pig.change_angle = -ANGLE
            self.pig.update()
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "S" and self.sheep_position == 0:
            self.sheep_center.remove_from_sprite_lists()
            self.sheep.set_pos(self.sheep.center_x, self.sheep.center_y)
            self.sheep_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "S" and self.sheep_position != 0:
            self.sheep.change_angle = ANGLE
            self.sheep.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "S" and self.sheep_position == 0:
            self.sheep_center.remove_from_sprite_lists()
            self.sheep.set_pos(self.sheep.center_x, self.sheep.center_y)
            self.sheep_position = 1
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "S" and self.sheep_position != 0:
            self.sheep.change_angle = -ANGLE
            self.sheep.update()
            self.card_select = None

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup_cow()
    window.setup_horse()
    window.setup_pig()
    window.setup_sheep()
    arcade.run()


if __name__ == "__main__":
    main()
