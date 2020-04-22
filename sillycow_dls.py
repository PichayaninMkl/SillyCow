from sillycowInit import Players

import os
from copy import deepcopy
from operator import itemgetter
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple

# Logging
log = None

# Percept ***
player = None
deck = None
trash = None
farm = ''

# State & Memorized variable
solution_list = {}
frontier = []
max_stack = 0 # For memory measuring
explored_state = []

DEPTH_LIMIT = 10

draw_src = 0 # 0 = trash, 1 = deck
draw_history = []
run_history = []

# -------------------------------------- Core --------------------------------------
def play(p:Players):
    global draw_src
    global max_stack
    global depth_limit
    global trash

    # Stack root state
    add_frontier(p, None, 0, 0) # No parent percept, inserting index = 0, depth = 0

    while frontier: # Loop until pop all stack's elements

        # Get expanding state & percept
        percept = select_frontier()
        p = set_percept(p, percept)
        state = percept['state']
        depth = percept['depth']

        # For logging
        parent = percept.get('parent')
        if parent:
            logging(f"\n<<< Expand <{state}> at depth ({depth}/{DEPTH_LIMIT}) from parent <{parent['state']}> >>>")
        else:
            logging(f"\n<<< Expand <{state}> at depth ({depth}/{DEPTH_LIMIT}) as Root >>>")
        logging(f'animal location :\n\tFarm = [{farm}]\n\tp[0] = [{player[0].field}]\n\tp[1] = [{player[1].field}]\n\tp[2] = [{player[2].field}]')
        

        # Found goal
        if (state == ('', 0, 0, 0, 0)):
            logging('>>> Goal!')
            update_solution(get_solution(percept), depth)
            continue

        # Hand out
        elif (state[1:] == (0, 0, 0, 0)):
            logging('>>> Hand out!')
            update_solution(get_solution(percept), DEPTH_LIMIT + depth + get_field_score(p.field))
            continue

        # Deck out
        elif deck == []:
            logging('>>> Deck out!')
            update_solution(get_solution(percept), 2 * DEPTH_LIMIT + depth + get_field_score(p.field))
            continue

        # Reach depth limit
        elif depth == DEPTH_LIMIT:
            logging('>>> Reach depth limit!')
            continue

        # Explore duplicated state, skip
        elif (state in explored_state):
            logging('>>> Duplicated state!')
            continue

        # Expand node
        else:
            # Add explored state
            explored_state.append(state)
            # Get inserting index
            index = len(frontier)
            # Increase depth
            depth += 1

            # Play pair card
            for ctype in p.hand.keys():
                if p.hand[ctype] >= 2:
                    animal_run(ctype, p, 'f')
                    add_frontier(p, percept, index, depth)
                    animal_run(ctype, p, 'r')

            # Play single card
            for ctype in p.hand.keys():
                if p.hand[ctype] >= 1:
                    card_operation(ctype, p, 'f')
                    add_frontier(p, percept, index, depth)
                    card_operation(ctype, p, 'r')
            
            # Play draw trash
            if trash != []:
                draw_trash(p, 'f')
                add_frontier(p, percept, index, depth)
                draw_trash(p, 'r')

            # Play draw deck
            if deck != []:
                draw_src = 1
                for ctype in p.hand.keys():
                    draw_deck(p, ctype, 'f') # simulative draw
                    add_frontier(p, percept, index, depth)
                    draw_deck(p, ctype, 'r')
                draw_src = 0


# -------------------------------------- Frontier & Percept & State --------------------------------------
def add_frontier(p:Players, parent_percept:Dict, index:int, depth:int):
    global frontier
    global draw_src
    global player
    global deck
    global trash
    global farm
    global max_stack
    
    state = (p.field, p.hand['S'], p.hand['P'], p.hand['H'], p.hand['C'])
    percept = {# Game percept
              'state':state,
              'draw':draw_src,
              'player':deepcopy(player),
              'deck':deepcopy(deck),
              'trash':deepcopy(trash), 
              'farm':farm,
               # Flow attribute
              'parent':parent_percept,
              'depth':depth}

    frontier.insert(index, percept)
    max_stack = max(len(frontier), max_stack)
    logging(f'=> Push <{state}> to Frontier at depth ({depth})')

def set_percept(p, percept:Dict) -> Players:
    global player
    global deck
    global trash
    global farm
    
    # Set env
    deck = percept['deck']
    trash = percept['trash']
    farm = percept['farm']
    
    # Set player
    i = player.index(p) # Find index from previous obj
    player = percept['player']
    return player[i]

def select_frontier() -> Dict:
    global frontier
    return frontier.pop() # Return percept state and remove expanded state
    
def get_action(percept:Dict) -> Tuple:
    return tuple(list(percept['state']) + [percept['draw']])

def get_solution(percept:Dict) -> Tuple:
    solution = [get_action(percept)]
    while percept['parent']:
        percept = percept['parent']
        solution.insert(0, get_action(percept))
    return tuple(solution)

def update_solution(solution:Tuple, cost:int):
    global solution_list

    if cost < solution_list.get(solution, np.inf):
        solution_list[solution] = cost
        logging(f'=>> Solution {solution} update with cost = {cost}\n')
    else:
        logging(f'=X> Solution {solution} NOT update by cost = {cost}\n')

# -------------------------------------- Action --------------------------------------
def animal_run(ctype:str, p:Players, flow:str):
    global trash
    global farm
    global player
    global run_history

    if flow == 'f':
        p.hand[ctype] -= 2
        trash.extend([ctype, ctype])
        logging(f'\n>> Discard 2 "{ctype}"\n\t {trash}')
        # move animal to destination
        if ctype in farm:
            logging(f'>> Move "{ctype}" from Farm -> p[{player.index(p.left)}]')
            logging(f'\t moving [{farm}],[{p.left.field}]')
            farm = farm.replace(ctype, '') # remove animal
            p.left.field += ctype # send animal
            run_history.append({'ctype':ctype, 'src':'farm', 'dest':p.left})
            logging(f'\t moved [{farm}],[{p.left.field}]')
        else:
            for p in player:
                if ctype in p.field:
                    logging(f'>> Move "{ctype}" from p[{player.index(p)}] -> p[{player.index(p.left)}]')
                    logging(f'\t moving [{p.field}],[{p.left.field}]')
                    p.field = p.field.replace(ctype, '') # remove animal
                    p.left.field += ctype # send animal
                    run_history.append({'ctype':ctype, 'src':p, 'dest':p.left})
                    logging(f'\t moved [{p.field}],[{p.left.field}]')
                    break

    elif flow == 'r':
        p.hand[ctype] += 2
        trash.pop()
        trash.pop()
        logging(f'<< Return 2 "{ctype}" to hand\n\t {trash}')

        # return animal to previours source
        animal = run_history.pop()
        dest_name = f'p[{player.index(animal["dest"])}]'
        dest0 = animal['dest'].field
        ct = animal['ctype']
        
        animal['dest'].field = animal['dest'].field.replace(animal['ctype'], '')
        if animal['src'] == 'farm':
            src_name = 'Farm'
            src0 = farm
            farm += animal['ctype']
            src1 = farm
        else:
            src_name = f'p[{player.index(animal["src"])}]'
            src0 = animal['src'].field
            animal['src'].field += animal['ctype']
            src1 = animal['src'].field
        
        dest1 = animal['dest'].field
        logging(f'<< Return "{ct}" from {dest_name} -> {src_name}')
        logging(f'\t returning [{dest0}],[{src0}]')
        logging(f'\t returned [{dest1}],[{src1}]')
    
# single card operation
def card_operation(ctype:str, p:Players, flow:str):
    global trash
    global player
    
    if flow == 'f':
        p.hand[ctype] -= 1
        trash.extend([ctype])
        logging(f'\n>> Discard a "{ctype}"')
        if ctype == 'S':
            pass
        elif ctype == 'P':
            draw_deck(p.left, ctype, flow) # p.left simulative draw, don't care ctype = "P"
            logging(f'\t p[{player.index(p.left)}] draw')
        elif ctype == 'H':
            draw_deck(p.right, ctype, flow)
            logging(f'\t p[{player.index(p.right)}] draw')
        elif ctype == 'C':
            draw_deck(p.left, ctype, flow)
            draw_deck(p.right, ctype, flow)
            logging(f'\t p[{player.index(p.left)}] and p[{player.index(p.right)}] draw')
        logging(f'\t {trash}')
            
    elif flow == 'r':
        p.hand[ctype] += 1
        trash.pop()
        logging(f'<< Return a "{ctype}" to Hand')
        if ctype == 'S':
            pass
        elif ctype == 'P':
            draw_deck(p.left, ctype, flow) # p.left simulative reverse draw
            logging(f'\t p[{player.index(p.left)}] return a card to Deck')
        elif ctype == 'H':
            draw_deck(p.right, ctype, flow) 
            logging(f'\t p[{player.index(p.right)}] return a card to Deck')
        elif ctype == 'C':
            draw_deck(p.left, ctype, flow)
            draw_deck(p.right, ctype, flow)
            logging(f'\t p[{player.index(p.left)}] and p[{player.index(p.right)}] return cards to Deck')
        logging(f'\t {trash}')

def draw_deck(p:Players, ctype:str, flow:str):
    global deck
    global draw_history
    global player
                  
    if flow == 'f':
        draw_history.append({'ctype':deck.pop(), 'src':deck}) # don't care the card, draw for deck out checking
        p.hand[ctype] += 1
        logging(f'\n>> p[{player.index(p)}] draw "{ctype}" from Deck')
    elif flow == 'r':
        card = draw_history.pop()
        deck.append(card['ctype']) # add the card to deck
        p.hand[ctype] -= 1
        logging(f'<< p[{player.index(p)}] return card "{ctype}" to Deck')
    
def draw_trash(p:Players, flow:str):
    global trash
    global draw_history
    global player
    
    if flow == 'f':
        draw_history.append({'ctype':trash.pop(), 'src':trash})
        card = draw_history[-1]
        p.hand[card['ctype']] += 1
        logging(f'\n>> p[{player.index(p)}] draw \"{card["ctype"]}\" from Trash\n\t {trash}')
    elif flow == 'r':
        card = draw_history.pop()
        trash.append(card['ctype']) # add the card to trash
        p.hand[card['ctype']] -= 1
        logging(f'<< p[{player.index(p)}] return card \"{card["ctype"]}\" to Trash\n\t {trash}')
    return card

# -------------------------------------- Score --------------------------------------
def get_field_score(field:str) -> int:
    # Score of each animal
    ctype_score = ['X', 'S', 'P', 'H', 'C']
    score = 0
    for ctype in field:
        score += ctype_score.index(ctype)
    return score

# -------------------------------------- Debuging --------------------------------------
def logging(text:str, end:str = '\n'):
    global log
    log.write(text + end)
    # print(text)
                
# -------------------------------------- Control --------------------------------------
def init_global_var():
    global log, solution_list, frontier, draw_src, max_stack, draw_history, run_history, explored_state
                  
    log = None
    solution_list = {}
    frontier = []
    draw_src = 0
    max_stack = 0
    draw_history = []
    run_history = []
    explored_state = []


def dls(p:Players, percept_player:List[Players], percept_deck:List, percept_trash:List,
          percept_farm:str) -> Tuple[Tuple]:
    global player
    global deck
    global trash
    global farm
    global solution_list
    global log

    init_global_var()
    player = percept_player
    deck = percept_deck
    trash = percept_trash
    farm = percept_farm
    
    # Time measuring
    start = datetime.now()
    ts = str(start)[:-7].replace(':', '-').replace(' ', '_')
    
    # Logging
    log_path = 'logging'
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log = open(f'{log_path}/dls-{ts}.txt', 'w', encoding='utf-8')
    
    play(p) # DLS iteration

    elapsed = datetime.now().timestamp() - start.timestamp()

    logging(f'\n------------------------- Summary -------------------------')
    # Select solution
    if not solution_list:
        logging(f'\nHave no Solution')
        sol = ()
    else:
        logging(f'\nAll Solution')
        solution_list = {k: v for k, v in sorted(solution_list.items(), key=lambda item: item[1])}
        for sol, cost in solution_list.items():
            logging(f'\nSolution {sol}\nCost = {cost}')
        sol = tuple(solution_list.items())[0][0]

    logging(f'\nSelect solution {sol}')
    logging(f'\nElapsed time = {elapsed} seconds\nMax Stack = {max_stack} nodes')
    log.close()
    return sol