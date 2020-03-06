import arcade
import os
import math
import time
import asyncio
from card import Card

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Silly Cow"

ANGLE = 120
test = 0
HAND = [2,3,3,1]
HAND1 = [3,2,3,1]
HAND2 = [2,3,2,2]
USED_DECK = []
DECK = ["C","H","P","S","C","H","P","S"]
COMMAND = [["H",2,False,False,1],[None,0,False,True,1],[None,0,True,False,1],[None,0,True,False,1],[None,0,True,False,1],[None,0,True,False,1]]
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
        self.hand_list1 = arcade.SpriteList()
        self.hand_list2 = arcade.SpriteList()
        self.top_used_card_list = arcade.SpriteList()
        self.deck_list = arcade.SpriteList()
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
        self.temp_hand_card1 = []
        self.temp_hand_card2 = []
        self.button = None
        self.deck = None
        self.top_used_card = None
        self.command_no = 0
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
        # print("card in hand :",len(self.hand_list))

    def setup_hand1(self,hand):
        list_name = ["C","H","P","S"]
        j = 0
        for i in range(4):
            for card_number in range(hand[i]):
                self.temp_hand_card1.append(None)
                self.temp_hand_card1[j] = Card(self.animal_picture_center[list_name[i]],SPRITE_SCALING)
                self.temp_hand_card1[j].center_x = 300  
                self.temp_hand_card1[j].center_y = 300 + (j*60)
                self.hand_list1.append(self.temp_hand_card1[j])
                j = j+1
        j = 0
        # print("card in hand1 :",len(self.hand_list))

    def setup_hand2(self,hand):
        list_name = ["C","H","P","S"]
        j = 0
        for i in range(4):
            for card_number in range(hand[i]):
                self.temp_hand_card2.append(None)
                self.temp_hand_card2[j] = Card(self.animal_picture_center[list_name[i]],SPRITE_SCALING)
                self.temp_hand_card2[j].center_x = 1300  
                self.temp_hand_card2[j].center_y = 300 + (j*60)
                self.hand_list2.append(self.temp_hand_card2[j])
                j = j+1
        j = 0
        # print("card in hand2 :",len(self.hand_list))

    def clear_hand(self):
        for i in range(len(self.hand_list)):
            self.hand_list.remove(self.temp_hand_card[i])
        

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

    def setup_deck(self):
        self.deck = Card(self.animal_picture_center[DECK[-1]],SPRITE_SCALING)
        self.deck.center_x = 400
        self.deck.center_y = (SCREEN_HEIGHT/2)
        self.deck_list.append(self.deck)

    def setup_used_deck(self):
        print("used card:",len(USED_DECK))
        if len(USED_DECK)>=1:
            print("have use card:",USED_DECK[-1])
            self.top_used_card = Card(self.animal_picture_center[USED_DECK[-1]],SPRITE_SCALING)
            self.top_used_card.center_x = 1200
            self.top_used_card.center_y = (SCREEN_HEIGHT/2)
            self.top_used_card_list.append(self.top_used_card) 
        else:
            print("don't have use card")
            # self.top_used_card = Card(self.animal_picture_center["C"],SPRITE_SCALING)
            # self.top_used_card.center_x = 1200
            # self.top_used_card.center_y = SCREEN_HEIGHT/2
            # self.top_used_card_list.append(self.top_used_card) 
    
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all card at center.
        self.card_list.draw()
        self.hand_list.draw()
        self.hand_list1.draw()
        self.hand_list2.draw()

        self.deck_list.draw()
        self.top_used_card_list.draw()
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
        self.playing(COMMAND[self.command_no])
        self.command_no+=1

    def playing(self, command):
        card = command[0]
        amount = command[1]
        draw_blind = command[2]
        draw = command[3]
        player = command[4]
        mapper = ["C","H","P","S"]
        """Called whenever a key is pressed. """
        print(amount,card,"Player:",player)
        if draw == True:
            # Draw used card
            HAND[mapper.index(USED_DECK[-1])] += 1
            self.clear_hand()
            self.setup_hand(HAND)
            self.hand_list.draw()
            self.setup_used_deck()
            self.top_used_card_list.draw()
            USED_DECK.pop()
        elif draw_blind == True and len(DECK)>=1:
            # Draw used card
            HAND[mapper.index(DECK[-1])] += 1
            self.clear_hand()
            self.setup_hand(HAND)
            self.hand_list.draw()   
            self.setup_deck()
            self.deck_list.draw()
            DECK.pop()
        elif HAND[mapper.index(card)]<amount:
            # Check if card(s) in hand is suffiecient to play
            print("cannot play.Not enough card")
        elif amount == 2 and self.animal_position_dict[card] == 0:
            # Move animal card for the first time
            self.center_all_dict[card].remove_from_sprite_lists()
            self.animal_all_dict[card].set_pos(self.animal_all_dict[card].center_x, self.animal_all_dict[card].center_y)
            self.animal_all_dict[card].change_angle = -(ANGLE * player)
            self.animal_all_dict[card].update()                
            self.animal_position_dict[card] = 1
            HAND[mapper.index(card)] -= amount
            for i in range(amount):
                USED_DECK.append(card) # Send used card to used Deck

            self.clear_hand()
            self.setup_hand(HAND)
            self.hand_list.draw()
            print("last used card:",USED_DECK[-1])
            self.setup_used_deck()
            self.top_used_card_list.draw()
        elif amount == 2 and self.animal_position_dict[card] == 1:
            # Move animal card
            self.animal_all_dict[card].change_angle = -ANGLE
            self.animal_all_dict[card].update()

        else:
            print("bug i sus")


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_buttons()
    window.setup_used_deck()
    window.setup_deck()
    window.setup_hand(HAND)
    window.setup_hand1(HAND1)
    window.setup_hand2(HAND2)

    window.setup_all_animal()
    arcade.run()

if __name__ == "__main__":
    main()
