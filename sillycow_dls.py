from sillycowInit import Players
from graphviz import Digraph

import os
from datetime import datetime
from typing import List, Dict, Tuple

# Graph visualization
dot = Digraph(comment='Agent Decision')
parent_node = None
previous_node = None
action_label = ''

# Logging
log = None

# Percept
player = None
deck = None
trash = None
farm = ''

# State & Memorized variable
#     action:cost 
#     action = stack of all action for completed or terminal path
#     cost = level (hop count)      ; if finish at goal
#          = depth limit (max cost) ; if finish at other
#     * always replace with lower cost in duplicate action
solution = {}

action_stack = []
visited_state = []
node_id = 0 # For memory measuring

draw_src = 0 # 0 = trash, 1 = deck
draw_history = []
run_history = []

depth_limit = 10
depth = -1

def init_global_var():
    global dot, parent_node, previous_node, action_label, log, \
            player, deck, trash, farm, solution, \
            action_stack, visited_state, node_id, draw_src, draw_history, \
            run_history, depth_limit, depth

    dot = Digraph(comment='Agent Decision')
    parent_node = None
    previous_node = None
    action_label = ''
    log = None
    player = None
    deck = None
    trash = None
    farm = ''
    solution = {}
    action_stack = []
    visited_state = []
    node_id = 0
    draw_src = 0
    draw_history = []
    run_history = []
    depth_limit = 10
    depth = -1

def play(p:Players):
    global depth
    global depth_limit
    global action_stack
    global visited_state
    global node_id
    global parent_node
    global previous_node
    global action_label
    global draw_src
    
    depth += 1
    state = (p.field, p.hand['S'], p.hand['P'], p.hand['H'], p.hand['C'])
    action_stack.append(tuple(list(state) + [draw_src]))
    draw_src = 0
    current_node = f'Node{node_id}'
    node_id += 1
    
    logging(f'\n<<< Play <{state}> at depth ({depth}/{depth_limit}) >>>')
    
    # Found goal
    if (state == ('', 0, 0, 0, 0)):
        create_node(current_node, f'{state}\nGoal!', 'doublecircle', 'green')
        logging('>>> Goal!')
        update_solution(tuple(action_stack), depth)
        
    # Hand out
    elif (state[1:] == (0, 0, 0, 0)):
        create_node(current_node, f'{state}\nHand out!', 'doublecircle', 'lightblue')
        logging('>>> Hand out!')
        update_solution(tuple(action_stack), depth_limit + depth)
        
    # Deck out
    elif deck == []:
        create_node(current_node, f'{state}\nDeck out!', 'doublecircle', 'blue')
        logging('>>> Deck out!')
        update_solution(tuple(action_stack), 2 * depth_limit + depth)
    
    # Reach depth limit
    elif depth == depth_limit:
        create_node(current_node, f'{state}\nReach limit!', 'circle', 'red')
        logging('>>> Reach depth limit!')
        
    # Check visited state
    elif state in visited_state:
        create_node(current_node, f'{state}\nDuplicated!', 'circle', 'gray')
        logging(f'>>> Duplicated state! <{state}>\n')
    
    # Play
    else:
        visited_state.append(state)
        
        create_node(current_node, f'{state}', 'circle')

        # Play pair card
        for ctype in p.hand.keys():
            if p.hand[ctype] >= 2:
                action_label = f'discard 2 "{ctype}"'
                logging(f'>> Play pair "{ctype}"')
                animal_run(ctype, p, 'f')
                play(p)
                animal_run(ctype, p, 'r')
                logging(f'\n<<< Backtracked <{state}> at depth ({depth}/{depth_limit}) >>>')
                parent_node = current_node

        # Play single card
        for ctype in p.hand.keys():
            if p.hand[ctype] >= 1:
                action_label = f'discard 1 "{ctype}"'
                logging(f'>> Play single "{ctype}"')
                card_operation(ctype, p, 'f')
                play(p)
                card_operation(ctype, p, 'r')
                logging(f'\n<<< Backtracked <{state}> at depth ({depth}/{depth_limit}) >>>')
                parent_node = current_node
        
        # Play draw trash
        if trash != []:
            action_label = f'draw Trash "{trash[-1]}"'
            logging(f'>> Play draw \"{trash[-1]}\" from Trash')
            draw_trash(p, 'f')
            play(p)
            draw_trash(p, 'r')
            logging(f'\n<<< Backtracked <{state}> at depth ({depth}/{depth_limit}) >>>')
        
        # Play draw deck
        for ctype in p.hand.keys():
            # simulative draw
            action_label = f'draw Deck "{ctype}"'
            logging(f'>> Play draw "{ctype}" from Deck')
            draw_src = 1
            draw_deck(p, ctype, 'f')
            play(p)
            draw_deck(p, ctype, 'r')
            draw_src = 0
            logging(f'\n<<< Backtracked <{state}> at depth ({depth}/{depth_limit}) >>>')
    
    parent_node = previous_node
    action_stack.pop()
    depth -= 1

def animal_run(ctype: chr, p:Players, flow:str):
    global trash
    global farm
    global player
    global run_history

    if flow == 'f':
        p.hand[ctype] -= 2
        trash.extend([ctype, ctype])
        logging(f'>F discard 2 "{ctype}"\n\t {trash}')
        # move animal to destination
        if ctype in farm:
            logging(f'>F move "{ctype}" from Farm -> p[{player.index(p.left)}]')
            logging(f'\t moving [{farm}],[{p.left.field}]')
            farm = farm.replace(ctype, '') # remove animal
            p.left.field += ctype # send animal
            run_history.append({'ctype':ctype, 'src':'farm', 'dest':p.left})
            logging(f'\t moved [{farm}],[{p.left.field}]')
        else:
            for p in player:
                if ctype in p.field:
                    logging(f'>F move "{ctype}" from p[{player.index(p)}] -> p[{player.index(p.left)}]')
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
        logging(f'<R return 2 "{ctype}" to hand\n\t {trash}')

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
        logging(f'<R return "{ct}" from {dest_name} -> {src_name}')
        logging(f'\t returning [{dest0}],[{src0}]')
        logging(f'\t returned [{dest1}],[{src1}]')
    
# single card operation
def card_operation(ctype: chr, p:Players, flow:str):
    global trash
    
    if flow == 'f':
        p.hand[ctype] -= 1
        trash.extend([ctype])
        logging(f'>F discard a "{ctype}"')
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
        logging(f'<R return a "{ctype}" to Hand')
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
                  
    if flow == 'f':
        draw_history.append({'ctype':deck.pop(), 'src':deck}) # don't care the card, draw for deck out checking
        p.hand[ctype] += 1
        logging(f'>F draw "{ctype}" from Deck')
    elif flow == 'r':
        card = draw_history.pop()
        deck.append(card['ctype']) # add the card to deck
        p.hand[ctype] -= 1
        logging(f'<R return card "{ctype}" to Deck')
    
def draw_trash(p:Players, flow:str):
    global trash
    global draw_history
    
    if flow == 'f':
        draw_history.append({'ctype':trash.pop(), 'src':trash})
        card = draw_history[-1]
        p.hand[card['ctype']] += 1
        logging(f'>F draw \"{card["ctype"]}\" from Trash\n\t {trash}')
    elif flow == 'r':
        card = draw_history.pop()
        trash.append(card['ctype']) # add the card to trash
        p.hand[card['ctype']] -= 1
        logging(f'<R return card \"{card["ctype"]}\" to Trash\n\t {trash}')
    return card

def get_clearing_ctype(field: str) -> str:
    for ctype in 'CHPS': # check field according type's priority
        if ctype in field:
            return ctype
              
def update_solution(action: Tuple, cost: int):
    global solution
    global depth_limit

    if cost < solution.get(action, 3 * depth_limit + 1): # if have no the state, put certainly
        solution[action] = cost
        logging(f'=>> Solution {action} update with cost = {cost}\n')
    else:
        logging(f'=X> Solution {action} NOT update by cost = {cost}\n')
              
def create_node(node_name:str, label:str, shape:str = 'circle', color:str = 'black'):
    global dot
    global parent_node
    global previous_node
    global action_label
        
    # If root node
    if not parent_node:
        label += '\nRoot'
        shape = 'doublecircle'
        color = 'yellow'
    
    # Create new node
    dot.attr('node', shape=shape, color=color)
    dot.node(node_name, f'{node_name}\n{label}')
    
    # Link with parent node
    if parent_node:
        dot.edge(parent_node, node_name, label=action_label)
    
    # Set currnet node to parent node
    previous_node = parent_node
    parent_node = node_name
              
def logging(text:str):
    global log                
    log.write(text + '\n')

def dls(p:Players, percept_player:List[Players], percept_deck:List, percept_trash:List, percept_farm:str) -> Tuple[Tuple]:
    global player
    global deck
    global trash
    global farm
    global solution
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
    
    # DLS recursion
    play(p) 

    elapsed = datetime.now().timestamp() - start.timestamp()
    dot.save(f'graphviz/dls-{ts}.gv') # Save graph

    # Select solution
    if not solution:
        logging(f'\nHave no Solution')
        sol = ()
    else:
        solution = {k: v for k, v in sorted(solution.items(), key=lambda item: item[1])}
        for sol, cost in solution.items():
            logging(f'\nSolution {sol}\nCost = {cost}')
        sol = tuple(solution.items())[0][0]

    logging(f'\nSelect solution {sol}')
    print(f'\nElapsed time = {elapsed} seconds\nCreated node = {node_id} nodes')                
    logging(f'\nElapsed time = {elapsed} seconds\nCreated node = {node_id} nodes')                
    log.close()
    return sol