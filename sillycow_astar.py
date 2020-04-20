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
known_hand = None

# State & Memorized variable
solution_list = {}
frontier = []
depth = 0
max_depth = 0 # For memory measuring
explored_state = []

draw_src = 0 # 0 = trash, 1 = deck
draw_history = []
run_history = []

# -------------------------------------- Core --------------------------------------
def play(p:Players):
    global depth
    global draw_src
    global max_depth
    global trash

    # Stack root state
    heu_cost = heuristic_cost(p)
    stack_percept(p, None, 0, heu_cost) # No parent percept, actual cost = 0

    while frontier: # Loop until pop all stack's elements

        # Get expanding state & percept
        percept = select_frontier()
        p = set_percept(p, percept)
        state = percept['state']

        # For logging
        parent = percept.get('parent')
        if parent:
            logging(f"\n<<< Expand <{state}> cost ({percept['act_cost']} + {percept['heu_cost']} = {percept['cost']}) from parent <{parent['state']}> ({parent['act_cost']} + {parent['heu_cost']} = {parent['cost']}) >>>")
        else:
            logging(f"\n<<< Expand <{state}> cost ({percept['cost']}) as Root >>>")
        logging(f'animal location :\n\tFarm = [{farm}]\n\tp[0] = [{player[0].field}]\n\tp[1] = [{player[1].field}]\n\tp[2] = [{player[2].field}]')


        # Found goal
        if (state == ('', 0, 0, 0, 0)):
            logging('>>> Goal!')
            update_solution(get_solution(percept), percept['cost'])
            break

        # Hand out
        elif (state[1:] == (0, 0, 0, 0)):
            logging('>>> Hand out!')
            update_solution(get_solution(percept), percept['cost'])
        
        # Explore duplicates state, skip
        elif (state in explored_state):
            continue

        # Expand node
        else:
            # Stack new level state
            depth = percept['depth'] + 1
            max_depth = max(depth, max_depth)
            # Add explored state
            explored_state.append(state)

            # Play pair card
            for ctype in p.hand.keys():
                if p.hand[ctype] >= 2:
                    act_cost = actual_cost(p, ctype, 'd2', percept['act_cost'])
                    animal_run(ctype, p, 'f')
                    heu_cost = heuristic_cost(p)
                    stack_percept(p, percept, act_cost, heu_cost)
                    animal_run(ctype, p, 'r')

            # Play single card
            for ctype in p.hand.keys():
                if p.hand[ctype] >= 1:
                    act_cost = actual_cost(p, ctype, 'd1', percept['act_cost'])
                    card_operation(ctype, p, 'f')
                    heu_cost = heuristic_cost(p)
                    stack_percept(p, percept, act_cost, heu_cost)
                    card_operation(ctype, p, 'r')
            
            # Play draw trash
            if trash != []:
                act_cost = actual_cost(p, trash[-1], 'dt', percept['act_cost'])
                draw_trash(p, 'f')
                heu_cost = heuristic_cost(p)
                stack_percept(p, percept, act_cost, heu_cost)
                draw_trash(p, 'r')

            # Play draw deck
            if deck != []:
                draw_src = 1
                for ctype in p.hand.keys():
                    act_cost = actual_cost(p, ctype, 'dd', percept['act_cost'])
                    draw_deck(p, ctype, 'f') # simulative draw
                    heu_cost = heuristic_cost(p)
                    stack_percept(p, percept, act_cost, heu_cost)
                    draw_deck(p, ctype, 'r')
                draw_src = 0


# -------------------------------------- Frontier & Percept & State --------------------------------------
def stack_percept(p:Players, parent_percept:Dict, act_cost:float, heu_cost:int):
    global frontier
    global depth
    global draw_src
    global player
    global deck
    global trash
    global farm
    
    state = (p.field, p.hand['S'], p.hand['P'], p.hand['H'], p.hand['C'])
    percept = {# Game percept
              'state':state,
              'draw':draw_src,
              'player':deepcopy(player),
              'deck':deepcopy(deck),
              'trash':deepcopy(trash), 
              'farm':farm,
               # Flow attribute 
              'act_cost':act_cost,
              'heu_cost':heu_cost,
              'cost':act_cost+heu_cost,
              'parent':parent_percept,
              'depth':depth}

    frontier.append(percept)
    logging(f'=> Push <{state}> to Frontier with cost ({act_cost} + {heu_cost} = {act_cost+heu_cost})')

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
    percept = sorted(frontier, key=itemgetter('cost'))[0]
    frontier.remove(percept) # Remove expanded state
    return percept # Return percept state
    
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

# -------------------------------------- Cost --------------------------------------
  
# g(n) : cumulative cost from root to node n ***calculate before state change***
def actual_cost(p:Players, ctype:str, action_type:str, cumulative_cost:float) -> float:
    global deck
    global trash
    global farm
    
    # Score of each animal
    ctype_score = ['', 'S', 'P', 'H', 'C']
    
    if action_type == 'd2':
        # Dis2_eq = CardName[“A”] * (dis2 * (minn + (3*R[“A”] + 2*F[“A”] + L[“A”]) + (L[“A”]) +
        #           (3*(R[“A”] and !Enough_card[“A”]))))
        cost = ctype_score.index(ctype) * (1 + (3*(ctype in p.right.field) + 2*(ctype in farm) + (ctype in p.left.field)) + (ctype in p.left.field) + \
              (3*((ctype in p.right.field) and not (p.hand[ctype] >= 4))))
    elif action_type == 'd1':
        # Dis1_eq = dis1 * (midd + (3*Clearing[“A”] + 2*R[“A”] + F[“A”]) + 
        #           (2*(R[“A”] and !Enough_card[“A”])))
        cost = 2 + (3*(ctype in p.field) + 2*(ctype in p.right.field) + (ctype in farm)) + \
              (2*((ctype in p.right.field) and not (p.hand[ctype] >= 3)))
    elif action_type == 'dt':
        # Draw_trash_eq = Draw_trash * (more + max(3*L[“A”] + 2*F[“A”] + R[“A”], 10*Enough_card[“A”]) - 
        #                 (2*(Trash[“A”] and R[“A”] and (card[“A”] == 1))))
        cost = 3 + max((3*(ctype in p.left.field) + 2*(ctype in farm) + (ctype in p.right.field)), 10*(p.hand[ctype] >= 2)) - \
              (2*((ctype in p.right.field) and (p.hand[ctype] == 1)))
    elif action_type == 'dd':
        # Draw_Deck_eq = Draw_Deck * (maxx - (2*NumberOfTargetCard[“A”]/RemainDeck * 
        #                (R[“A”] and (card[“A”] == 1))))
        cost = 4 - (2 * (18 - (p.hand[ctype] + known_hand['L'][ctype] + known_hand['R'][ctype])) / len(deck) * \
              ((ctype in p.right.field) and (p.hand[ctype] == 1)))

    logging(f"\n+> Actual cost <{action_type.upper()}{ctype}> ({(p.field, p.hand['S'], p.hand['P'], p.hand['H'], p.hand['C'])}) = {cumulative_cost} + {cost} = {cumulative_cost + cost}")
    return cumulative_cost + cost

# h(n) : shortest path from node n to goal (least turn) ***calculate after state change***
def heuristic_cost(p:Players) -> int:
    global farm

    sim_farm = farm
    sim_field = [p.field, p.left.field, p.right.field]
    sim_phand = deepcopy(p.hand)
    cost = 0

    for ctype, ncard in sim_phand.items():
        # Discard 2
        played_turn = int(np.floor(ncard/2))
        cost += played_turn
        sim_phand[ctype] %= 2 # After this, card left <= 1

        # Flow animal
        if played_turn > 0:
            # Find animal for move
            if ctype in farm:
                farm.replace(ctype, '')
                animal_pos = 0
            else:
                for i in range(len(sim_field)):
                    if ctype in sim_field[i]:
                        sim_field[i].replace(ctype, '')
                        animal_pos = i
                        break
            # Move animal
            sim_field[(animal_pos + played_turn)%len(sim_field)] += ctype

        # Check field
        if ctype in sim_field[0]:
            # Clear field
            if ncard >= 2: # ncard is started card
                cost = (cost - 1) + (2 + sim_phand[ctype]) # Back 1 turn then play rest card (1 card/turn)
            else:
                cost += 3 - sim_phand[ctype] # Find & discard 2 (2 turns)
            sim_phand[ctype] = 0
        else:
            # Play rest card
            cost += sim_phand[ctype] # Discard 1 | Not play

    logging(f"\n+> Heuristic cost ({(p.field, p.hand['S'], p.hand['P'], p.hand['H'], p.hand['C'])}) = {cost}\n")    
    return cost

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

# -------------------------------------- Debuging --------------------------------------
def logging(text:str, end:str = '\n'):
    global log
    log.write(text + end)
    # print(text)
                
# -------------------------------------- Control --------------------------------------
def init_global_var():
    global log, solution_list, draw_src, max_depth, draw_history, run_history, depth_limit, depth, explored_state, frontier
                  
    log = None
    solution_list = {}
    draw_src = 0
    max_depth = 0
    draw_history = []
    run_history = []
    depth = 0
    depth_limit = 10
    explored_state = []
    frontier = []

def astar(p:Players, percept_player:List[Players], percept_deck:List, percept_trash:List,
          percept_farm:str, percept_known_hand:Dict[str,Dict]) -> Tuple[Tuple]:
    global player
    global deck
    global trash
    global farm
    global known_hand
    global solution_list
    global log

    init_global_var()
    player = percept_player
    deck = percept_deck
    trash = percept_trash
    farm = percept_farm
    known_hand = percept_known_hand
    
    print("Know:",known_hand)
    print("hand:",p.hand)
    print("farm:",percept_farm)
    print("field:",p.field)
    # Time measuring
    start = datetime.now()
    ts = str(start)[:-7].replace(':', '-').replace(' ', '_')
    
    # Logging
    log_path = 'logging'
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log = open(f'{log_path}/dls-{ts}.txt', 'w', encoding='utf-8')
    
    play(p) # A* iteration

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
    logging(f'\nElapsed time = {elapsed} seconds\nMax Depth = {max_depth+1} levels (0 - {max_depth})') # Depth include root
    log.close()
    print("Solution!", sol)
    return sol