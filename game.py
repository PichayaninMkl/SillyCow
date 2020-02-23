import arcade
import os
import math

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Silly Cow"

ANGLE = 120

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

    def set_pos(self):
        # print(self.center_x, self.center_y)
        self.center_y = SCREEN_HEIGHT / 2
        self.center_x = SCREEN_WIDTH / 2
        

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
        self.cow_list_center = None
        self.horse_list_center = None
        self.pig_list_center = None
        self.sheep_list_center = None
        # self.cow_list = None
        # self.horse_list = None
        # self.pig_list = None
        # self.sheep_list = None

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

        # card select
        self.card_select = None

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup_cow(self):
        """ Set up the game and initialize the variables. """

        self.cow_list_center = arcade.SpriteList()
        self.cow_center = Card("card/cow_center.png", SPRITE_SCALING)
        self.cow_center.center_x = (SCREEN_WIDTH / 2)-150
        self.cow_center.center_y = SCREEN_HEIGHT / 2
        self.cow_list_center.append(self.cow_center)

        # self.cow_list = arcade.SpriteList()
        self.cow = Card("card/cow.png", SPRITE_SCALING)
        self.cow.center_x = SCREEN_WIDTH / 2
        self.cow.center_y = (SCREEN_HEIGHT / 2)+400
        # self.cow_list.append(self.cow)

    def setup_horse(self):
        self.horse_list_center = arcade.SpriteList()
        self.horse_center = Card("card/horse_center.png", SPRITE_SCALING)
        self.horse_center.center_x = (SCREEN_WIDTH / 2)-50
        self.horse_center.center_y = SCREEN_HEIGHT / 2
        self.horse_list_center.append(self.horse_center)

        # self.horse_list = arcade.SpriteList()
        self.horse = Card("card/horse.png", SPRITE_SCALING)
        self.horse.center_x = SCREEN_WIDTH / 2
        self.horse.center_y = (SCREEN_HEIGHT / 2)+400
        # self.horse_list.append(self.horse)

    def setup_pig(self):
        self.pig_list_center = arcade.SpriteList()
        self.pig_center = Card("card/pig_center.png", SPRITE_SCALING)
        self.pig_center.center_x = (SCREEN_WIDTH / 2)+50
        self.pig_center.center_y = SCREEN_HEIGHT / 2
        self.pig_list_center.append(self.pig_center)

        # self.pig_list = arcade.SpriteList()
        self.pig = Card("card/pig.png", SPRITE_SCALING)
        self.pig.center_x = SCREEN_WIDTH / 2
        self.pig.center_y = (SCREEN_HEIGHT / 2)+400
        # self.pig_list.append(self.pig)

    def setup_sheep(self):
        self.sheep_list_center = arcade.SpriteList()
        self.sheep_center = Card("card/sheep_center.png", SPRITE_SCALING)
        self.sheep_center.center_x = (SCREEN_WIDTH / 2)+150
        self.sheep_center.center_y = SCREEN_HEIGHT / 2
        self.sheep_list_center.append(self.sheep_center)

        # self.sheep_list = arcade.SpriteList()
        self.sheep = Card("card/sheep.png", SPRITE_SCALING)
        self.sheep.center_x = SCREEN_WIDTH / 2
        self.sheep.center_y = (SCREEN_HEIGHT / 2)+400
        # self.sheep_list.append(self.sheep)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all card at center.
        self.cow_list_center.draw()
        self.horse_list_center.draw()
        self.pig_list_center.draw()
        self.sheep_list_center.draw()
        self.cow.draw()
        self.horse.draw()
        self.pig.draw()
        self.sheep.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        # self.cow_list.update()
        pass

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
            self.cow.set_pos()
            self.cow_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "C" and self.cow_position != 0:
            self.cow.change_angle = ANGLE
            self.cow.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "C" and self.cow_position == 0:
            self.cow_center.remove_from_sprite_lists()
            self.cow.set_pos()
            self.cow_position = 1
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "C" and self.cow_position != 0:
            self.cow.change_angle = -ANGLE
            self.cow.update()
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "H" and self.horse_position == 0:
            self.horse_center.remove_from_sprite_lists()
            self.horse.set_pos()
            self.horse_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "H" and self.horse_position != 0:
            self.horse.change_angle = ANGLE
            self.horse.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "H" and self.horse_position == 0:
            self.horse_center.remove_from_sprite_lists()
            self.horse.set_pos()
            self.horse_position = 1
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "H" and self.horse_position != 0:
            self.horse.change_angle = -ANGLE
            self.horse.update()
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "P" and self.pig_position == 0:
            self.pig_center.remove_from_sprite_lists()
            self.pig.set_pos()
            self.pig_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "P" and self.pig_position != 0:
            self.pig.change_angle = ANGLE
            self.pig.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "P" and self.pig_position == 0:
            self.pig_center.remove_from_sprite_lists()
            self.pig.set_pos()
            self.pig_position = 1
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "P" and self.pig_position != 0:
            self.pig.change_angle = -ANGLE
            self.pig.update()
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "S" and self.sheep_position == 0:
            self.sheep_center.remove_from_sprite_lists()
            self.sheep.set_pos()
            self.sheep_position = 1
            self.card_select = None
        elif key == arcade.key.LEFT and self.card_select == "S" and self.sheep_position != 0:
            self.sheep.change_angle = ANGLE
            self.sheep.update()
            self.card_select = None
        elif key == arcade.key.RIGHT and self.card_select == "S" and self.sheep_position == 0:
            self.sheep_center.remove_from_sprite_lists()
            self.sheep.set_pos()
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