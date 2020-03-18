import arcade
import os
import math
import time
import asyncio
from card import Card
from button import TextButton
import sillycowInit as sillycow
from sillycow_dls import dls
from bfs import BFS


def converter(hand):
    listOfHand = []
    listOfHand.insert(0, hand['S'])
    listOfHand.insert(1, hand['P'])
    listOfHand.insert(2, hand['H'])
    listOfHand.insert(3, hand['C'])
    return listOfHand


# *************************************** Set GAME *****************************************
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Silly Cow"
ANGLE = 120
test = 0
# ******************************************************************************************

# *************************************** Set CARD *****************************************
HAND = []
USED_DECK = []
DECK = sillycow.create_deck()
farm = 'SPHC'
n_player = 3
player = sillycow.create_player(3, DECK)
# player[0].left = player[1]
# player[1].left = player[2]
# player[1].left = player[0]
# player[0].right = player[2]
# player[2].right = player[1]
# player[1].right = player[0]

for i in range(3):
    inputHand = converter(player[i].hand)
    HAND.insert(i, inputHand)
    i += 1
# ******************************************************************************************

#  card = command[0]
#         amount = command[1]
#         draw_blind = command[2]
#         draw = command[3]
#         player = command[4]

# *************************************** Ai action dls ************************************
action=[]


def check_action(action: list, animal: str, old, new,hand_now,player : int):
    if new == old+1:
        if hand_now[5] == 1:
            action.append([animal,0,True,False,player])
        elif hand_now[5] == 0:
            action.append([animal,0,False,True,player])
    elif new == old-2:
        action.append([animal,2,False,False,player])
    elif new == old-1:
        action.append([animal,1,False,False,player])

def dls_play(player):
    action=[]
    player_dls = player.copy()
    DECK_dls = DECK.copy()
    trash = USED_DECK.copy()
    # print(player[1].hand)
    A = dls(player_dls[1], player_dls, DECK_dls, trash, farm)
    # print(A)
    count = 0
    animal =""
    num = 0
    for i in A:
        # print("hand : ", i)
        if count == 0:
            check_hand = i
            count += 1
            # print("***************************************************")        
        else:
            if check_hand[1] != i[1]:
                animal = "S"
                num = 1
            elif check_hand[2] != i[2]:
                animal = "P"
                num = 2
            elif check_hand[3] != i[3]:
                animal = "H"
                num = 3
            elif check_hand[4] != i[4]:
                animal = "C"
                num = 4
            else:
                check_hand = i
            check_action(action,animal,check_hand[num],i[num],i,1)
            check_hand = i
        #     print(action)
        #     print("***************************************************")
        # print("old : ", check_hand)
    print("DLS:",action)
    return action

# ******************************************************************************************

# *************************************** Ai action bfs ************************************
def bfs_play(player):
    action=[]
    player_bfs = player.copy()
    DECK_bfs = DECK.copy()
    trash = USED_DECK.copy()
    # print(player[1].hand)
    A = BFS(player_bfs[2], player_bfs, farm, DECK_bfs, trash)
    # print(A)
    count = 0
    animal =""
    num = 0
    for i in A:
        # print("hand : ", i)
        if count == 0:
            check_hand = i
            count += 1
            # print("***************************************************")        
        else:
            if check_hand[1] != i[1]:
                animal = "S"
                num = 1
            elif check_hand[2] != i[2]:
                animal = "P"
                num = 2
            elif check_hand[3] != i[3]:
                animal = "H"
                num = 3
            elif check_hand[4] != i[4]:
                animal = "C"
                num = 4
            else:
                check_hand = i
            check_action(action,animal,check_hand[num],i[num],i,2)
            check_hand = i
        #     print(action)
        #     print("***************************************************")
        # print("old : ", check_hand)
    print("BFS:",action)    
    return action
# ******************************************************************************************
# print(bfs_play(player))
# COMMAND = [["H", 2, False, False, 0],
#            [None, 0, False, True, 1],
#            ["H", 2, True, False, 2],
#            [None, 0, True, False, 0],
#            ["P", 2, False, False, 1],
#            [None, 0, False, True, 2]]
# COMMAND = [[None, 0, False, True, 1],
#            ["H", 2, True, False, 2],
#            ["P", 2, False, False, 1],
#            [None, 0, False, True, 2]]

class PlayTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function,text):
        super().__init__(center_x, center_y, 100, 40, text, 24, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

    def on_press(self):
        super().on_press()
        self.action_function()

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
        self.hand_list = [arcade.SpriteList(), arcade.SpriteList(
        ), arcade.SpriteList()]  # all card in player's hand
        # each card in player's hand
        self.temp_hand_card = [[None], [None], [None]]
        self.list_name = ["S", "P", "H", "C"]

        self.player_p = 0

        self.top_used_card_list = arcade.SpriteList()
        self.top_used_card = None

        self.deck_list = arcade.SpriteList()
        self.deck = None
        self.deck_text = None
        self.trash_text = None
        self.mat = None

        self.hand_temp = [None,0]
        self.field_temp = None
        self.animal_center_temp = None

        self.start_sim = False
        # Set up the Card info
        self.card_list = arcade.SpriteList()
        self.cow_center = None
        self.horse_center = None
        self.pig_center = None
        self.sheep_center = None

        self.cow = None
        self.horse = None
        self.pig = None
        self.sheep = None

        self.button = None
        self.text_player_0 = None
        self.text_key_press = None
        self.text_no_card = None
        self.no_card = False
        self.key_player_0 = None
        self.command_no = 0  # in case of having list of command

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
        # This button will do every command in COMMAND list
        # button_temp = arcade.TextButton(
        #     100, 100, 150, 50, "Play", font_size=24)
        # self.button = arcade.SubmitButton(
        #     button_temp, self.on_submit, 100, 150, text="Play")
        sim_name = "Sim:"+ str(self.player_p)
        self.button = PlayTextButton(150, 150,self.on_submit, text = "Play")
        self.button2 = PlayTextButton(150, 50,self.on_submit2, text = sim_name)

    def set_decktrash_text(self):
        self.deck_text = arcade.draw_text("Deck",380,(SCREEN_HEIGHT/2)+20,arcade.color.WHITE,16)
        self.trash_text = arcade.draw_text("Trash",1180,(SCREEN_HEIGHT/2)+20,arcade.color.WHITE,16)
        


    def set_text(self):
        
        self.text_player_0 = arcade.draw_text("C:Use 2 cow  \
            H:Use 2 horse   \
            P:Use 2 pig \
            S:Use 2 sheep   \
            L:Use 1 cow \
            M:Use 1 horse   \
            N:Use 1 pig \
            O:Use 1 sheep   \
            Z:Draw  \
            X:Draw blind"\
            , 20, 40, arcade.color.WHITE, 16)
        self.text_key_press = arcade.draw_text("------ Please Enter Key ------",0, 70, arcade.color.WHITE, 18, width=SCREEN_WIDTH, align="center")
        self.text_no_card = arcade.draw_text("Cannot play. Not enough card!!!",0, 10, arcade.color.RED, 22, width=SCREEN_WIDTH, align="center")

    def setup_hand(self, hand):
        # print("hand are:",hand)
        j = 0
        for player in range(3):
            for i in range(4):
                for card_number in range(hand[player][i]):
                    self.temp_hand_card[player].append(None)
                    self.temp_hand_card[player][j] = Card(
                        self.animal_picture_center[self.list_name[i]], SPRITE_SCALING)
                    self.temp_hand_card[player][j].center_x = 300 + \
                        (j*60*(player == 0)) + 1000*(player == 2)
                    self.temp_hand_card[player][j].center_y = 150 + \
                        (j*40)*(player > 0) + 200*(player > 0)
                    self.hand_list[player].append(
                        self.temp_hand_card[player][j])
                    j = j+1
            j = 0
        # print("card in hand :",len(self.hand_list))

    def clear_hand(self):
        # Clear all player's hand every turn
        self.hand_list.clear()
        self.hand_list = [arcade.SpriteList(), arcade.SpriteList(),
                          arcade.SpriteList()]

    def setup_all_animal(self):
        counter = -3
        for name in self.list_name:
            self.center_all_dict[name] = Card(
                self.animal_picture_center[name], SPRITE_SCALING)
            self.center_all_dict[name].center_x = (
                SCREEN_WIDTH/2) + (counter*50)
            self.center_all_dict[name].center_y = (SCREEN_HEIGHT/2)
            self.card_list.append(self.center_all_dict[name])

            self.animal_all_dict[name] = Card(
                self.animal_picture_rotate[name], SPRITE_SCALING)
            self.animal_all_dict[name].center_x = SCREEN_WIDTH * \
                (0.4+(0.01*(counter+4)))
            # print(name," position: ",self.animal_all_dict[name].)
            counter = counter + 2

    def setup_deck(self):
        self.deck = Card(self.animal_picture_center[DECK[-1]], SPRITE_SCALING)
        self.deck.center_x = 400
        self.deck.center_y = (SCREEN_HEIGHT/2)+100
        self.deck_list.append(self.deck)

    def setup_used_deck(self):
        # print("used card:",len(USED_DECK))
        if len(USED_DECK) >= 1:
            # print("have use card:",USED_DECK[-1])
            self.top_used_card = Card(
                self.animal_picture_center[USED_DECK[-1]], SPRITE_SCALING)
            self.top_used_card.center_x = 1200
            self.top_used_card.center_y = (SCREEN_HEIGHT/2)+100
            self.top_used_card_list.append(self.top_used_card)
        else:
            print("don't have use card")

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        arcade.draw_rectangle_filled((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2),700,500,arcade.color.REDWOOD)
        self.deck_text.draw()
        self.trash_text.draw()
        # Draw all card at center.
        self.card_list.draw()
        for player in range(3):
            self.hand_list[player].draw()
        # self.hand_list1.draw()
        # self.hand_list2.draw()

        self.deck_list.draw()
        self.top_used_card_list.draw()
        for name in self.list_name:
            self.animal_all_dict[name].draw()
        # self.button.draw()

        if self.player_p == 0:
            
            self.text_key_press.draw()
            self.text_player_0.draw()

        if self.key_player_0 != None or self.player_p != 0:
            self.button.draw()
            self.button.pressed = False

        if self.no_card:
            self.text_no_card.draw()

        if self.player_p != 0:
            self.button2.draw()
            self.button2.pressed = False

    def on_update(self, delta_time):
        if(self.start_sim and (self.command_no < len(action))):
            # print("Command No:",self.command_no,"len action",len(action)-1)
            self.simulatinng()
        elif (self.command_no == len(action) and len(action) != 0) and self.start_sim :
            self.command_no = 0
            self.start_sim = False
            print("done simulating")
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        # self.cow_list.update()
        

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.button.check_mouse_press(x, y)
        self.button2.check_mouse_press(x, y)


    

    # def on_mouse_release(self, x, y, buttons, modifiers):
    #     self.button.check_mouse_release(x, y)
    def reset_sim(self):
        if(self.hand_temp[1] == self.player_p and self.player_p != 0):
            # print(self.hand_temp[0],"player:",self.player_p)
            self.setup_used_deck()
            self.top_used_card_list.draw()
            HAND[self.player_p] = self.hand_temp[0]
            self.animal_position_dict = self.animal_center_temp
            counter = -3
            
            for animal in self.list_name:
                
                self.animal_all_dict[animal].angle = 0
                if(self.animal_center_temp[animal]==0):
                    # print(animal,"was at a center")
                    self.center_all_dict[animal] = Card(
                        self.animal_picture_center[animal], SPRITE_SCALING)
                    self.center_all_dict[animal].center_x = (
                        SCREEN_WIDTH/2) + (counter*50)
                    self.center_all_dict[animal].center_y = (SCREEN_HEIGHT/2)
                    self.card_list.append(self.center_all_dict[animal])
                    # self.card_list.draw()

                    self.animal_all_dict[animal].remove_from_sprite_lists()
                    self.animal_all_dict[animal] = Card(
                        self.animal_picture_rotate[animal], SPRITE_SCALING)
                    self.animal_all_dict[animal].center_x = SCREEN_WIDTH * \
                        (0.4+(0.01*(counter+4)))
                else:
                    # print(animal,"was at ",self.field_temp[animal])
                    self.animal_all_dict[animal].change_angle = self.field_temp[animal]
                    # self.animal_all_dict[animal].angle = 0
                    self.animal_all_dict[animal].update()
                    for name in self.list_name:
                        # print(name,"angle:",self.field_temp[name])
                        self.animal_all_dict[name].draw()
                counter += 2
            
            self.hand_temp = [None,0]
            self.command_no = 0
            self.setup_hand(HAND)
            self.hand_list[self.player_p].draw()
            self.card_list.draw()
        else:
            self.command_no = 0
            pass

    def on_submit(self):
        self.start_sim = False
        if self.player_p!=0:
            self.reset_sim()
            self.playing(action[0])
        else:
            self.playing(None)
        
    def on_submit2(self):
        self.reset_sim()
        # print("All action:",action)
        # print("Command No:",self.command_no,"len action",len(action)-1)
        self.hand_temp = [HAND[self.player_p].copy(),self.player_p]
        # print("hand_temp player",self.player_p,self.hand_temp)
        
        self.field_temp = {
            "S":self.animal_all_dict["S"].get_angle(),
            "P":self.animal_all_dict["P"].get_angle(),
            "H":self.animal_all_dict["H"].get_angle(),
            "C":self.animal_all_dict["C"].get_angle()
        }
        self.animal_center_temp = self.animal_position_dict.copy()
        self.start_sim = True
        print("Start sim",self.start_sim,"animal center",self.animal_center_temp)
        
        
            
    def simulatinng(self):
        
        self.playing(action[self.command_no])
        time.sleep(1)
 #   ********************************************************* "PREPARE SEARCH" ********************************************************        
    def prepare_search(self):
        global action
        global player

        for i in range(3):
            player[i].hand = {
                'S': HAND[i][0],
                'P': HAND[i][1],
                'H': HAND[i][2],
                'C': HAND[i][3]
            }
            # player[i].field = 
        
        if self.player_p==0:
            # prepare dls while player 0 is playing
            print("player 1 field(DLS)",player[1].field)
            action = dls_play(player)

            # print("Percept for player:",1,"Field",player[1].field,"Hand:",player[1].hand)
        elif self.player_p == 1 and self.start_sim!=True:
            print("player 2 field(BFS)",player[2].field)
            # prepare bfs while player 1 (bot) is playing
            action = bfs_play(player)
            # print("BFS:",action)
#   ********************************************************* "PLAYING" ******************************************************** 
    def playing_draw(self, player):
        if len(DECK) >= 1:
            # Draw used card
            HAND[player][self.list_name.index(DECK[-1])] += 1
            self.clear_hand()
            self.setup_hand(HAND)
            self.hand_list[player].draw()
            self.setup_deck()
            self.deck_list.draw()
            DECK.pop()
            print("Player:", player, " draw blind")
            
        return True

    def playing(self, command):   
        global player
        global farm

        if self.player_p==0:
            command = None
            command = self.key_player_0
            self.no_card = False
        else:
            self.command_no += 1

        if command!=None:
            card = command[0]
            amount = command[1]
            draw_blind = command[2]
            draw = command[3]
            self.player_p = command[4]
            # print("Sim?:",self.start_sim,"hand card before",HAND[self.player_p])
            """Called whenever a key is pressed. """
            # print(amount,card,"Player:",player)
            if (draw == True and len(USED_DECK) >= 1) and self.start_sim != True:
                # Draw used card
                HAND[self.player_p][self.list_name.index(USED_DECK[-1])] += 1
                self.clear_hand()
                self.setup_hand(HAND)
                self.hand_list[self.player_p].draw()
                self.setup_used_deck()
                self.top_used_card_list.draw()
                USED_DECK.pop()
                print("Player:", self.player_p, " draw")
                self.prepare_search()
                # self.command_no += 1
            elif self.start_sim == True and (draw == True or draw_blind == True):
                HAND[self.player_p][self.list_name.index(card)] += 1
                self.clear_hand()
                self.setup_hand(HAND)
                self.hand_list[self.player_p].draw()
                
                print("Player:", self.player_p, "think it's draw:",card)
                # self.command_no += 1
            elif draw_blind == True and len(DECK) >= 1:
                # Draw used card
                HAND[self.player_p][self.list_name.index(DECK[-1])] += 1
                self.clear_hand()
                self.setup_hand(HAND)
                self.hand_list[self.player_p].draw()
                self.setup_deck()
                self.deck_list.draw()
                DECK.pop()
                print("Player:", self.player_p, " draw blind")
                self.prepare_search()
                # self.command_no += 1
            elif HAND[self.player_p][self.list_name.index(card)] < amount:
                # Check if card(s) in hand is suffiecient to play
                print("Player:", self.player_p, " cannot play.Not enough card")
                if self.player_p == 0:
                    self.no_card = True
                    self.key_player_0 = None 
            elif amount == 1:
                HAND[self.player_p][self.list_name.index(card)] -= amount
                USED_DECK.append(card)
                self.clear_hand()
                self.setup_hand(HAND)
                self.hand_list[self.player_p].draw()
                # print("last used card:",USED_DECK[-1])
                self.setup_used_deck()
                self.top_used_card_list.draw()
                print("Player:", self.player_p, " used ", card)
                if self.start_sim == True:
                    USED_DECK.pop()
                else:
                    # check card
                    if card == "H":
                        #right hand
                        if self.player_p < 0:
                            p = self.player_p - 1
                        else:
                            p = 2
                        self.playing_draw(p)
                    elif card == "C":
                        player_n = [0,1,2]
                        for i in range(len(player_n)):
                            if player_n[i] != self.player_p:
                                self.playing_draw(player_n[i])
                    elif card == "P":
                        #left hand
                        if self.player_p < 2:
                            p = self.player_p + 1
                        else:
                            p = 0
                        self.playing_draw(p)
                self.prepare_search()
                # self.command_no += 1        
            elif amount == 2 and self.animal_position_dict[card] == 0:
                # Move animal card for the first time
                self.center_all_dict[card].remove_from_sprite_lists()
                self.animal_all_dict[card].set_pos(
                    self.animal_all_dict[card].center_x, self.animal_all_dict[card].center_y)
                self.animal_all_dict[card].change_angle = -(ANGLE * (self.player_p+1))
                self.animal_all_dict[card].update()
                self.animal_position_dict[card] = 1
                if self.start_sim!=True:
                    player[self.player_p].left.field +=  card  # update player field percept
                    farm.replace(card,'')

                HAND[self.player_p][self.list_name.index(card)] -= amount
                for i in range(amount):
                    USED_DECK.append(card)  # Send used card to used Deck
                    self.setup_used_deck()
                    self.top_used_card_list.draw()
                    if self.start_sim == True  :
                        USED_DECK.pop()
                self.clear_hand()
                self.setup_hand(HAND)
                self.hand_list[self.player_p].draw()
                # print("last used card:",USED_DECK[-1])
                # print("hand card after:",HAND[self.player_p])
                self.prepare_search()
                print("Player:", self.player_p, " move ", card)
                # self.command_no += 1
            elif amount == 2 and self.animal_position_dict[card] == 1:
                # Move animal card
                self.animal_all_dict[card].change_angle = -ANGLE
                self.animal_all_dict[card].update()
                for i in range(3):
                    if(player[i].field.find(card)!= -1 and self.start_sim!=True):
                        print("Found",card,"on player",i,"field :",player[i].field)
                        player[i].left.field += card
                        player[i].field = player[i].field.replace(card,'')
                        
                        break

                HAND[self.player_p][self.list_name.index(card)] -= amount
                for i in range(amount):
                    USED_DECK.append(card)  # Send used card to used Deck
                    self.setup_used_deck()
                    self.top_used_card_list.draw()
                    if self.start_sim == True  :
                        USED_DECK.pop()
                self.clear_hand()
                self.setup_hand(HAND)
                self.hand_list[self.player_p].draw()
                self.prepare_search()
                # self.command_no += 1
                # print("hand card after:",HAND[self.player_p])
                print("Player:", self.player_p, " move ", card)
            else:
                print("bug i sus")

            if not self.no_card and self.start_sim!=True:
                if self.player_p!=2:
                    self.player_p += 1
                else:
                    self.player_p = 0
                self.key_player_0 = None
            self.set_buttons()

            return True

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.C:
            self.key_player_0 = ["C", 2, False, False, 0]
        elif key == arcade.key.H:
            self.key_player_0 = ["H", 2, False, False, 0]
        elif key == arcade.key.P:
            self.key_player_0 = ["P", 2, False, False, 0]
        elif key == arcade.key.S:
            self.key_player_0 = ["S", 2, False, False, 0]
        elif key == arcade.key.L:
            self.key_player_0 = ["C", 1, False, False, 0]
        elif key == arcade.key.M:
            self.key_player_0 = ["H", 1, False, False, 0]
        elif key == arcade.key.N:
            self.key_player_0 = ["P", 1, False, False, 0]
        elif key == arcade.key.O:
            self.key_player_0 = ["S", 1, False, False, 0]
        elif key == arcade.key.Z:
            self.key_player_0 = [None, 0, False, True, 0]
        elif key == arcade.key.X:
            self.key_player_0 = [None, 0, True, False, 0]

        return True       

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_buttons()
    window.set_text()
    window.set_decktrash_text()
    window.setup_used_deck()
    window.setup_deck()
    window.setup_hand(HAND)
    window.setup_all_animal()
    

    arcade.run()


if __name__ == "__main__":
    main()
