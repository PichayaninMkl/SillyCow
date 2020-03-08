import numpy as np
import random
from typing import List, Dict, Tuple

class Players:
    field = '' # str
    hand = None # Dict
    left = None # Players
    right = None # Players

def generate_hand(n:int, order:int, n_step:int) -> Dict:
    global deck
    h = {'S':0, 'P':0, 'H':0, 'C':0}
    n_deck = len(deck)
    
    # draw from the top deck (backward draw from list)
    for i in range(n_deck-1-order, n_deck-1-n*n_step, -n_step):
        ctype = deck[i]
        h[ctype] += 1
    return h
        
def create_player(n_player:int) -> List:
    global deck
    n_hand = 9
    
    pl = [Players() for i in range(n_player)]
    for i in range(n_player):
        pl[i].hand = generate_hand(n_hand, i, n_player)
        # link player object
        pl[i].left = pl[(i+1)%n_player]
        pl[i].right = pl[i-1]
        
    deck = deck[:-(n_hand*n_player)] # remove drawn card
    return pl

def create_deck() -> List:
    deck = []
    n_card = {'S':18, 'P':18, 'H':18, 'C':18}
    for ctype, n in n_card.items():
        deck.extend([ctype] * n)
    random.shuffle(deck)
    return deck
