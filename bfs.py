from writelog import write_log, close_log
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

    def is_equal(self, node):
        boolean1 = (self.field == node.field)
        boolean2 = (self.hand_sheep == node.hand_sheep)
        boolean3 = (self.hand_pig == node.hand_pig)
        boolean4 = (self.hand_horse == node.hand_horse)
        boolean5 = (self.hand_cow == node.hand_cow)
        return boolean1 and boolean2 and boolean3 and boolean4 and boolean5
        # return False


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
    frontier = [root_node]
    explored = []

    solution = [[], 0]

    # For debug
    current_depth = 0

    count = 0
    count_dup = 0

    while len(frontier) > 0:
        count += 1

        this_node = frontier.pop(0)
        this_node["ref_num"] = count

        explored.append(this_node)
        write_log("Exploring >> Node : " + str(this_node["ref_num"]))
        # write_log("Depth : " + str(this_node["depth"]))
        # write_log(str(this_node["player"]))
        # write_log(str(this_node["field"]))

        player = this_node["player"]
        field = this_node["field"]
        depth = this_node["depth"]

        ref_num = count

        # Final state
        if player.field == "" and player.hand_sheep + player.hand_pig + player.hand_horse + player.hand_cow == 0:
            goal_state = explored[-1]
            path = [goal_state]
            prev = goal_state['parent']
            while prev is not None:
                prev_node = explored[prev - 1]
                prev = prev_node['parent']
                path.append(prev_node)
            path.reverse()
            write_log("\t>> Goal state")
            return [path, len(explored)]
        if player.hand_sheep + player.hand_pig + player.hand_horse + player.hand_cow == 0:
            write_log("\t>> Hand out")
            continue
        elif len(field.deck) == 0:
            print("\t>> Deck out")
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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

            if player.hand_horse >= 1:
                out = discard_H(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_H"
                }
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

            if player.hand_cow >= 1:
                out = discard_C(player, field)
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "discard_C"
                }
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

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
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

                out = draw_deck(player, field, 'P')
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_deck_P"
                }
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

                out = draw_deck(player, field, 'H')
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_deck_H"
                }
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)

                out = draw_deck(player, field, 'C')
                next_node = {
                    "ref_num": -1,
                    "player": out["player"],
                    "field": out["field"],
                    "parent": ref_num,
                    "depth": depth + 1,
                    "action": "draw_deck_C"
                }
                is_duplicate = False
                for node in explored + frontier:
                    if next_node["player"].is_equal(node["player"]):
                        is_duplicate = True
                        write_log("\t^^^ Duplicate Node")
                        count_dup += 1
                if not is_duplicate:
                    frontier.append(next_node)
                # is_duplicate = False
                # for n in explored + frontier:
                #     next_left = next_node["field"].left
                #     next_right = next_node["field"].right
                #     left = n["field"].left
                #     right = n["field"].right
                #     if next_node["player"] == n["player"] and next_left == left and next_right == right:
                #         is_duplicate = True
                #         # write_log("\t^^^ Duplicate Node")
                #         print("\t>> Duplicate node")
                #         count_dup += 1
                # if not is_duplicate:
                #     frontier.append(next_node)
    return solution


# def BFS(player,player_list, farm, deck, trash):
def BFS(player, player_list, farm, deck, trash):
    print("Percept from BFS(player 2)","Field",player.field,"Hand:",player.hand)

    start_time = time.time()
    # psutil.cpu_percent()
    # psutil.virtual_memory()
    # mem = dict(psutil.virtual_memory()._asdict())

    left_field = player.left.field
    right_field = player.right.field

    # root_node = Node(field, hand['S'], hand['P'], hand['H'], hand['C'])
    root_node = Node(player.field, player.hand['S'], player.hand['P'], player.hand['H'], player.hand['C'])
    root_field = Field(left_field, right_field, farm, deck, trash)

    out = searching(root_node, root_field)
    path = out.copy()[0]
    n_node = out.copy()[1]

    runtime = time.time() - start_time
    write_log("")
    write_log(get_str_action_path(path))
    print("Run-time : " + str('%.4f' % runtime) + " seconds")
    print("Node(s) : " + str(n_node))
    write_log("Run-time : " + str('%.4f' % runtime) + " seconds")
    write_log("Node(s) : " + str(n_node))
    # logging("Space usage : " + str(math.ceil(mem['used'] / (1024 ** 2))) + " Mb")

    solution = []
    for n in path:
        node = n["player"]
        action = n["action"]
        draw_state = 0
        if action is not None and (action[5:9] == "deck"):
            draw_state = 1
        solution.append(tuple([node.field, node.hand_sheep, node.hand_pig, node.hand_horse, node.hand_cow, draw_state]))
    solution = tuple(solution)
    write_log("")
    write_log(str(solution))
    close_log()
    return solution


# ( / )
def discard_2S(player, field):
    write_log("\t >>> DO ACTION : Discard 2 Sheep cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_sheep -= 2
    field.trash.append('S')
    field.trash.append('S')

    return animal_run('S', player, field)


def discard_2P(player, field):
    write_log("\t >>> DO ACTION : Discard 2 Pig cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_pig -= 2
    field.trash.append('P')
    field.trash.append('P')

    return animal_run('P', player, field)


def discard_2H(player, field):
    write_log("\t >>> DO ACTION : Discard 2 Horse cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_horse -= 2
    field.trash.append('H')
    field.trash.append('H')

    return animal_run('H', player, field)


def discard_2C(player, field):
    write_log("\t >>> DO ACTION : Discard 2 Cow cards")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_cow -= 2
    field.trash.append('C')
    field.trash.append('C')

    return animal_run('C', player, field)


def discard_S(player, field):
    write_log("\t >>> DO ACTION : Discard a Sheep card")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_sheep -= 1
    field.trash.append('S')

    return {
        "player": player,
        "field": field
    }


def discard_P(player, field):
    write_log("\t >>> DO ACTION : Discard a Pig card")

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


def discard_H(player, field):
    write_log("\t >>> DO ACTION : Discard a Horse card")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_horse -= 1
    field.trash.append('H')
    if len(field.deck) > 0:
        field.deck.pop(deck_top)

    return {
        "player": player,
        "field": field
    }


def discard_C(player, field):
    write_log("\t >>> DO ACTION : Discard a Cow card")

    player = Node(player.field, player.hand_sheep, player.hand_pig, player.hand_horse, player.hand_cow)
    field = Field(field.left, field.right, field.farm, field.deck.copy(), field.trash.copy())

    player.hand_cow -= 1
    field.trash.append('C')
    if len(field.deck) > 0:
        field.deck.pop(deck_top)
    if len(field.deck) > 0:
        field.deck.pop(deck_top)

    return {
        "player": player,
        "field": field
    }


def draw_trash(player, field):
    write_log("\t >>> DO ACTION : Draw a card (Top) from trash and skip")

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


def draw_deck(player, field, card):
    write_log("\t >>> DO ACTION : Draw a card (Random : " + card + " ) from deck and skip")

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


def animal_run(animal, player, field):
    if animal in player.field:
        player.field = player.field.replace(animal, "")
        field.left += animal
    elif animal in field.left:
        field.left = field.left.replace(animal, "")
        field.right += animal
    elif animal in field.right:
        field.right = field.right.replace(animal, "")
        player.field += animal
    else:
        field.farm = field.farm.replace(animal, "")
        field.left += animal
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
