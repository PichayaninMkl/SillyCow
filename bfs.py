from logging_ta import logging, close_log
import time

# import psutil
# import math

trash_top = -1
deck_top = -1


class Node:
    def __init__(self, field="", s=0, p=0, h=0, c=0):
        self.field = field
        self.hand_sheep = s
        self.hand_pig = p
        self.hand_horse = h
        self.hand_cow = c

    def __str__(self):
        return "----- Player status -----\nFIELD : " + str(self.field) + \
               "\nHAND  : <S=" + str(self.hand_sheep) + \
               " P=" + str(self.hand_pig) + \
               " H=" + str(self.hand_horse) + \
               " C=" + str(self.hand_cow) + ">\n------------------------"


class Field:
    def __init__(self, left, right, farm, deck, trash):
        self.left = left
        self.right = right
        self.farm = farm
        self.deck = deck
        self.trash = trash

    def __str__(self):
        out = "----- Field status -----\nLeft Field : " + self.left + "\nRight Field : " + self.right + "\n"
        if len(self.farm) > 0:
            out += "Farm : " + self.farm + "\n"
        out += "Deck : " + str(self.deck)[1:-1] + "\n"
        out += "Trash : " + str(self.trash)[1:-1] + "\n------------------------"
        return out


# lf = left field
# rf = right field
def searching(player_root, field_root):
    root_node = {
        "ref_num": -1,
        "player": player_root,
        "field": field_root,
        "parent": None,
        "depth": 0,
        "action": None,
    }

    # Breadth-First Search
    tree = []
    queue_list = [root_node]
    solution = []
    # duplicate = []
    current_depth = 0

    count = 0

    while len(queue_list) > 0:
        count += 1

        this_node = queue_list.pop(0)
        this_node["ref_num"] = count

        tree.append(this_node)
        logging("Node : " + str(this_node["ref_num"]))
        logging("Depth : " + str(this_node["depth"]))
        logging(str(this_node["player"]))
        logging(str(this_node["field"]))

        player = this_node["player"]
        field = this_node["field"]
        depth = this_node["depth"]

        ref_num = count

        # Final state
        if player.field == "" and player.hand_sheep + player.hand_pig + player.hand_horse + player.hand_cow == 0:
            goal_state = tree[-1]
            solution.append(goal_state)
            prev = goal_state['parent']
            while prev is not None:
                prev_node = tree[prev - 1]
                prev = prev_node['parent']
                solution.append(prev_node)
            solution.reverse()
            logging("\t>> Goal state")
            return [solution, len(tree)]
        elif player.hand_sheep + player.hand_pig + player.hand_horse + player.hand_cow == 0 and len(player.field) > 0:
            logging("\t>> Hand out")
            continue
        elif len(field.deck) == 0:
            logging("\t>> Deck out")
            continue
        else:
            if player.hand_sheep >= 2:
                out = discard_2S(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_2S"
                }
                queue_list.append(next_node)

            if player.hand_pig >= 2:
                out = discard_2P(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_2P"
                }
                queue_list.append(next_node)

            if player.hand_horse >= 2:
                out = discard_2H(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_2H"
                }
                queue_list.append(next_node)

            if player.hand_cow >= 2:
                out = discard_2C(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_2C"
                }
                queue_list.append(next_node)

            if player.hand_sheep >= 1:
                out = discard_S(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_S"
                }
                queue_list.append(next_node)

            if player.hand_pig >= 1:
                out = discard_P(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_P"
                }
                queue_list.append(next_node)

            if len(field.trash) > 0:
                out = draw_trash(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_trash"
                }
                queue_list.append(next_node)

            if len(field.deck) > 0:
                out = draw_deck(player, field, 'S')
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_deck_S"
                }
                queue_list.append(next_node)

                out = draw_deck(player, field, 'P')
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_deck_P"
                }
                queue_list.append(next_node)

                out = draw_deck(player, field, 'H')
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_deck_H"
                }
                queue_list.append(next_node)

                out = draw_deck(player, field, 'C')
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_deck_C"
                }
                queue_list.append(next_node)
                # is_dup = False
                # for node in duplicate:
                #     if node["player"] == next_node["player"] and node["field"] == next_node["field"]:
                #         print("Duplicate node")
                #         is_dup = True
                # if not is_dup:
                #     duplicate.append({
                #         "player": next_node["player"],
                #         "field": next_node["field"],
                #     })
                #     queue_list.append(next_node)


def BFS(player, player_list, farm, deck, trash):
    start_time = time.time()
    # psutil.cpu_percent()
    # psutil.virtual_memory()
    # mem = dict(psutil.virtual_memory()._asdict())
    
    left_field = player.left.field
    right_field = player.right.field

    root_node = Node(player.field, player.hand['S'], player.hand['P'], player.hand['H'], player.hand['C'])
    root_field = Field(left_field, right_field, farm, deck, trash)

    out = searching(root_node, root_field)
    path = out.copy()[0]
    n_node = out.copy()[1]

    runtime = time.time() - start_time
    logging("Run-time : " + str('%.4f' % runtime) + " seconds")
    logging("Node(s) : " + str(n_node))
    # logging("Space usage : " + str(math.ceil(mem['used'] / (1024 ** 2))) + " Mb")

    solution = []
    for n in path:
        node = n["player"]
        solution.append(tuple([node.field, node.hand_sheep, node.hand_pig, node.hand_horse, node.hand_cow]))
    solution = tuple(solution)
    logging("")
    logging(str(solution))
    close_log()
    return solution


# ( / )
def discard_2S(player, field):
    logging("\t >>> DO ACTION : Discard 2 Sheep cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_sheep -= 2
    field.trash.append('S')
    field.trash.append('S')

    if "S" in player.field:
        player.field = player.field.replace("S", "")
        field.left += "S"
    elif "S" in field.left:
        field.left = field.left.replace("S", "")
        field.right += "S"
    elif "S" in field.right:
        field.right = field.right.replace("S", "")
        player.field += "S"
    else:
        field.farm = field.farm.replace("S", "")
        field.left += "S"

    return {
        "player": player,
        "field": field
    }


# ( / )
def discard_2P(player, field):
    logging("\t >>> DO ACTION : Discard 2 Pig cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_pig -= 2
    field.trash.append('P')
    field.trash.append('P')

    if "P" in player.field:
        player.field = player.field.replace("P", "")
        field.left += "P"
    elif "P" in field.left:
        field.left = field.left.replace("P", "")
        field.right += "P"
    elif "P" in field.right:
        field.right = field.right.replace("P", "")
        player.field += "P"
    else:
        field.farm = field.farm.replace("P", "")
        field.left += "P"

    return {
        "player": player,
        "field": field
    }


# ( / )
def discard_2H(player, field):
    logging("\t >>> DO ACTION : Discard 2 Horse cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_horse -= 2
    field.trash.append('H')
    field.trash.append('H')

    if "H" in player.field:
        player.field = player.field.replace("H", "")
        field.left += "H"
    elif "H" in field.left:
        field.left = field.left.replace("H", "")
        field.right += "H"
    elif "H" in field.right:
        field.right = field.right.replace("H", "")
        player.field += "H"
    else:
        field.farm = field.farm.replace("H", "")
        field.left += "H"

    return {
        "player": player,
        "field": field
    }


# ( / )
def discard_2C(player, field):
    logging("\t >>> DO ACTION : Discard 2 Cow cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_cow -= 2
    field.trash.append('C')
    field.trash.append('C')

    if "C" in player.field:
        player.field = player.field.replace("C", "")
        field.left += "C"
    elif "C" in field.left:
        field.left = field.left.replace("C", "")
        field.right += "C"
    elif "C" in field.right:
        field.right = field.right.replace("C", "")
        player.field += "C"
    else:
        field.farm = field.farm.replace("C", "")
        field.left += "C"

    return {
        "player": player,
        "field": field
    }


# ( / )
def discard_S(player, field):
    logging("\t >>> DO ACTION : Discard a Sheep card")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_sheep -= 1
    field.trash.append('S')

    return {
        "player": player,
        "field": field
    }


# ( / )
def discard_P(player, field):
    logging("\t >>> DO ACTION : Discard a Pig cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_pig -= 1
    field.trash.append('P')
    if len(field.deck) > 0:
        field.deck.pop(deck_top)

    return {
        "player": player,
        "field": field
    }


# ( / )
def draw_trash(player, field):
    logging("\t >>> DO ACTION : Draw a card (Top) from trash and skip")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    card = field.trash.pop(trash_top)

    if card == 'S':
        player.hand_sheep += 1
    elif card == 'P':
        player.hand_pig += 1
    elif card == 'H':
        player.hand_horse += 1
    elif card == 'C':
        player.hand_cow += 1
    return {
        "player": player,
        "field": field
    }


# ( / )
def draw_deck(player, field, card):
    logging("\t >>> DO ACTION : Draw a card (Random : " + card + " ) from deck and skip")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    field.deck.pop(deck_top)

    if card == 'S':
        player.hand_sheep += 1
    elif card == 'P':
        player.hand_pig += 1
    elif card == 'H':
        player.hand_horse += 1
    elif card == 'C':
        player.hand_cow += 1
    return {
        "player": player,
        "field": field
    }


def get_str_action_path(solution):
    st = ""
    for n in solution:
        if n["action"] is None:
            st += "START"
        else:
            st += n["action"]
        st += " -> "
    st += "GOAL"
    return st


# s = BFS("", {"S": 2, "P": 0, "H": 0, "C": 0}, "", "", "SPHC", ["S", "S", "S", "S"], [])
# print(s)
