import arcade
import os
import math
from card import Card

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Silly Cow"

ANGLE = 120
test = 0
HAND = [2,3,3,1]

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
        self.hand_list = arcade.SpriteList()
        # Set up the Card info
        self.cow_center = None
        self.horse_center = None
        self.pig_center = None
        self.sheep_center = None
        self.cow = None
        self.horse = None
        self.pig = None
        self.sheep = None
        self.temp_hand_card = []
        self.button = None

        # set position all card
        self.cow_position = 0
        self.horse_position = 0
        self.pig_position = 0
        self.sheep_position = 0


        # for easy access, use dictionary
        self.center_all_dict = {
            "C": self.cow_center,
            "H": self.horse_center,
            "P": self.pig_center,
            "S": self.sheep_center
        }
        self.animal_all_dict = {
            "C": self.cow,
            "H": self.horse,
            "P": self.pig,
            "S": self.sheep
        }
        self.animal_position_dict = {
            "C": self.cow_position,
            "H": self.horse_position,
            "P": self.pig_position,
            "S": self.sheep_position
        }
        self.animal_picture_center = {
            "C": "card/cow_center.png",
            "H": "card/horse_center.png",
            "P": "card/pig_center.png",
            "S": "card/sheep_center.png"
        }
        self.animal_picture_rotate = {
            "C": "card/cow.png",
            "H": "card/horse.png",
            "P": "card/pig.png",
            "S": "card/sheep.png"
        }

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def set_buttons(self):
        button_temp = arcade.TextButton(100,100,150,50,"Play",font_size=24)
        self.button = arcade.SubmitButton(button_temp,self.on_submit,100,100,text="Play")

    def setup_hand(self,hand):
        list_name = ["C","H","P","S"]
        j = 0
        for i in range(4):
            for card_number in range(hand[i]):
                self.temp_hand_card.append(None)
                self.temp_hand_card[j] = Card(self.animal_picture_center[list_name[i]],SPRITE_SCALING)
                self.temp_hand_card[j].center_x = 300  + (j*60)
                self.temp_hand_card[j].center_y = 100
                self.hand_list.append(self.temp_hand_card[j])
                j = j+1
        j = 0
        print(len(self.temp_hand_card))

    def clear_hand(self):
        print(len(self.hand_list))
        for i in range(len(self.hand_list)):
            self.hand_list.remove(self.temp_hand_card[i])
        print(len(self.hand_list))
        

    def setup_all_animal(self):
        counter = -3
        list_name = ["C","H","P","S"]
        for name in list_name:
            self.center_all_dict[name] = Card(self.animal_picture_center[name],SPRITE_SCALING)
            self.center_all_dict[name].center_x = (SCREEN_WIDTH/2) + (counter*50)
            self.center_all_dict[name].center_y = (SCREEN_HEIGHT/2)
            self.card_list.append(self.center_all_dict[name])

            self.animal_all_dict[name] = Card(self.animal_picture_rotate[name],SPRITE_SCALING)
            self.animal_all_dict[name].center_x = SCREEN_WIDTH * (0.4+(0.05*(counter+4)))
            # print(name," position: ",self.animal_all_dict[name].)
            counter = counter + 2

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all card at center.
        self.card_list.draw()
        self.hand_list.draw()
        list_name = ["C","H","P","S"]
        for name in list_name:
            self.animal_all_dict[name].draw()
        self.button.draw()


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        # self.cow_list.update()
        pass

    def on_mouse_press(self,x,y,buttons,modifiers):
        self.button.check_mouse_press(x,y)

    def on_mouse_release(self,x,y,buttons,modifiers):
        self.button.check_mouse_release(x,y)

    def on_submit(self):
        self.playing("H",2,False,False,1)


    def playing(self, card, amount,draw_blind,draw,player):
        mapper = ["C","H","P","S"]
        """Called whenever a key is pressed. """
        print(amount,card,player,self.animal_position_dict[card])
        if HAND[mapper.index(card)]<amount:
            print("cannot play.Not enough card")
        elif amount == 2 and self.animal_position_dict[card] == 0:
            self.center_all_dict[card].remove_from_sprite_lists()
            self.animal_all_dict[card].set_pos(self.animal_all_dict[card].center_x, self.animal_all_dict[card].center_y)
            self.animal_all_dict[card].change_angle = -(ANGLE * player)
            self.animal_all_dict[card].update()                
            self.animal_position_dict[card] = 1
            HAND[mapper.index(card)] -= amount
            self.clear_hand()
            self.setup_hand(HAND)
            self.hand_list.draw()
        elif amount == 2 and self.animal_position_dict[card] == 1:
            self.animal_all_dict[card].change_angle = -ANGLE
            self.animal_all_dict[card].update()
            print("go on")
        else:
            print("bug i sus")


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_buttons()
    window.setup_hand(HAND)
    window.setup_all_animal()
    arcade.run()


if __name__ == "__main__":
    main()
