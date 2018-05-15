"""
Contains all function for Dungeon Crawler
Taken from previous projects "Combat Game", and "Maze Game"
"""

import numpy as np
import random

import dungeon_classes as dc


# Maze Navigation
def maze_initialization():
    # create all possible rooms
    rooms = [dc.Room([0, 0, 0, 0]),  # Closed room(0)
             dc.Room([1, 1, 1, 1]),  # Open room(1)
             dc.Room([1, 0, 1, 0]),  # NS corridor(2)
             dc.Room([0, 1, 0, 1]),  # EW corridor(3)
             dc.Room([1, 0, 0, 1]),  # NW corner(4)
             dc.Room([1, 1, 0, 0]),  # NE corner(5)
             dc.Room([0, 1, 1, 0]),  # SE corner(6)
             dc.Room([0, 0, 1, 1]),  # SW corner(7)
             dc.Room([1, 1, 0, 1]),  # EW with N tee(8)
             dc.Room([1, 1, 1, 0]),  # NS with E tee(9)
             dc.Room([0, 1, 1, 1]),  # EW with S tee(10)
             dc.Room([1, 0, 1, 1]),  # NS with W tee(11)
             dc.Room([1, 0, 0, 0]),  # N dead end(12)
             dc.Room([0, 1, 0, 0]),  # E dead end(13)
             dc.Room([0, 0, 1, 0]),  # S dead end(14)
             dc.Room([0, 0, 0, 1]),  # W dead end(15)
             ]
    # create list using room indexes (will be converted when chosen)
    maze_1 = [[13, 3, 10, 7, 14, 0, 0],
              [13, 3, 4, 5, 11, 0, 0],
              [6, 7, 6, 3, 8, 7, 0],
              [2, 5, 1, 3, 15, 2, 0],
              [5, 3, 8, 7, 6, 4, 0],
              [0, 0, 0, 5, 11, 0, 0],
              [0, 0, 0, 0, 5, 3, 15],
              ]
    maze_2 = [[13, 10, 3, 3, 7, 14, 0, 14, 0, 0, 0],
              [0, 2, 13, 3, 4, 2, 0, 2, 0, 0, 0],
              [0, 5, 10, 3, 7, 2, 0, 9, 3, 3, 7],
              [0, 13, 4, 6, 8, 4, 14, 12, 14, 0, 2],
              [0, 0, 6, 8, 3, 7, 2, 0, 5, 3, 11],
              [0, 13, 1, 3, 7, 12, 2, 6, 7, 13, 11],
              [0, 0, 2, 14, 5, 3, 8, 11, 5, 3, 4],
              [0, 0, 5, 4, 0, 13, 3, 4, 0, 0, 0],
              ]
    maze_3 = [[13, 3, 7, 13, 7, 0, 14],
              [14, 13, 8, 7, 2, 0, 2],
              [2, 6, 7, 5, 8, 7, 2],
              [5, 4, 5, 3, 3, 8, 4],
              ]

    # create list of mazes, choose random maze for game, convert maze indexes to rooms
    mazes = [maze_1, maze_2, maze_3]  # random maze not used at this time
    maze_choice = random.choice(range(0, len(mazes)))
    maze_layout = mazes[maze_choice]
    maze_layout = index_to_rooms(maze_layout, rooms)
    return maze_choice, maze_layout


def vizualize_maze(maze_to_draw):
    """
    Uses Box Drawing unicode (u2500 - u257F) to draw the maze_to_draw
    :param maze_to_draw: Maze to be visualized
    :return: UI printout of maze_to_draw
    """

    # Create dictionary for box drawing unicode lookup
    # NOTE: each character uses a space before the symbol
    encoding = {0: ' \u2573',  # Closed room
                1: ' \u253C',  # Open room
                2: ' \u2502',  # NS corridor
                3: ' \u2500',  # EW corridor
                4: ' \u2518',  # NW corner
                5: ' \u2514',  # NE corner
                6: ' \u250C',  # SE corner
                7: ' \u2510',  # SW corner
                8: ' \u2534',  # EW with N tee
                9: ' \u251C',  # NS with E tee
                10: ' \u252C',  # EW with S tee
                11: ' \u2524',  # NS with W tee
                12: ' \u257D',  # N dead end
                13: ' \u257E',  # E dead end
                14: ' \u257F',  # S dead end
                15: ' \u257C',  # W dead end
                }

    # Determine shape of maze_to_draw
    x_len = len(maze_to_draw[0])
    y_len = len(maze_to_draw)

    draw = ['' for x in range(y_len)]
    # Encode maze_to_draw
    for i in range(0, x_len):  # columns
        for j in range(0, y_len):  # rows
            draw[j] += encoding[maze_to_draw[j][i]]

    for row in draw:
        print(row)
    print()


def random_maze(size):
    """
    Creates a random square maze of dimension = size
    :param size: Square dimension of desired maze
    :return: A list describing a random maze using index format
    """

    # Pad maze with 0 with zero index perimeter
    size += 2
    new_maze = np.empty((size, size))
    new_maze[0, :] = np.zeros((1, size))
    new_maze[-1, :] = np.zeros((1, size))
    new_maze[:, 0] = np.zeros(size)
    new_maze[:, -1] = np.zeros(size)

    # Define possible indexes for each compass direction (all options)
    north = [1, 2, 4, 5, 8, 9, 11, 12]
    east = [1, 3, 5, 6, 8, 9, 10, 13]
    south = [1, 2, 6, 7, 9, 10, 11, 14]
    west = [1, 3, 4, 7, 8, 10, 11, 15]

    # Set starting position
    new_maze[1][1] = 13

    # Loop through by row ensuring room connections
    for i in range(1, size - 1):

        for j in range(0, size - 2):
            # Determine if a connection is needed to adjacent rooms
            left_door = 1 if new_maze[i][j] in east else 0
            top_door = 1 if new_maze[i - 1][j + 1] in south else 0
            # bottom_door = 1 if new_maze[i + 1][j + 1] in north else 0
            # right_door = 1 if new_maze[i][j + 1] in west else 0

            if i < size - 2:  # for all rows above bottom row of actual maze

                if j < size - 3:  # for all columns before rightmost of actual maze

                    # Choose room at random that will connect with adjacent rooms
                    if left_door:
                        if top_door:
                            options = list(set(west) & set(north))

                        else:
                            options = list(set(west) - set(north))
                    else:
                        if top_door:
                            options = list(set(north) - set(west))

                        else:
                            options = list((set(south) & set(east)) - set(north) - set(west))

                else:

                    # Right edge of maze... can never go east
                    if left_door:
                        if top_door:
                            options = list((set(west) & set(north)) - set(east))

                        else:
                            options = list((set(west) - set(north)) - set(east))
                    else:
                        if top_door:
                            options = list(set(north) - set(west) - set(east))

                        else:
                            options = list(set(south) - set(north) - set(west) - set(east))

            else:  # Bottom edge of maze... can never go south

                if j < size - 3:  # for all columns before rightmost of actual maze

                    if left_door:
                        if top_door:
                            options = list((set(west) & set(north)) - set(south))

                        else:
                            options = list((set(west) - set(north)) - set(south))
                    else:
                        if top_door:
                            options = list(set(north) - set(west) - set(south))

                        else:
                            options = list(set(east) - set(west) - set(north) - set(south))

                else:
                    # Bottom right corner... can only go west and north
                    if left_door:
                        if top_door:
                            options = list((set(west) & set(north)) - set(south) - set(east))

                        else:
                            options = list((set(west) - set(north)) - set(south) - set(east))
                    else:
                        if top_door:
                            options = list(set(north) - set(west) - set(south) - set(east))

                        else:
                            options = [0]

            if i == 1 and j == 1:
                new_maze[1][1] = 13  # enforce starting position
                new_maze[i][j + 1] = random.choice(list(set(options) - {15}))  # make sure dead end not beside start
            else:
                new_maze[i][j + 1] = random.choice(options)

    # Extract actual maze
    new_maze = new_maze[1:-1, 1:-1]
    return np.ndarray.tolist(new_maze.astype(int))


def index_to_rooms(maze_x, rooms):
    """
    This function replaces maze lists of indexes with room objects
    :param maze_x: Maze to be recast into rooms
    :param rooms: List of possible rooms
    :return: List describing maze layout with room objects
    """
    i = 0
    for x in maze_x:
        j = 0

        for y in x:
            maze_x[i][j] = rooms[y]
            j += 1

        i += 1

    return maze_x


def move_loop(maze_layout, move, player):
    print('Where would you like to move?')

    direction = ''
    while not direction:
        direction = input('[N]orth, [E]ast, [S]outh, [W]est: ')

        if not direction:
            print("No input detected, please re-enter a direction\n")
            continue

    direction = direction.lower().strip()

    if direction == 'n':
        move = player.move(direction, maze_layout)
        if move:
            print(f'{player.name} moves north into the next room\n')

    elif direction == 'e':
        move = player.move(direction, maze_layout)
        if move:
            print(f'{player.name} moves east into the next room\n')

    elif direction == 's':
        move = player.move(direction, maze_layout)
        if move:
            print(f'{player.name} moves south into the next room\n')

    elif direction == 'w':
        move = player.move(direction, maze_layout)
        if move:
            print(f'{player.name} moves west into the next room\n')

    else:
        print(f"Sorry, the command {direction} was not recognized. Please re-enter a command.\n")

    return move


# Combat Game
def rest(d8, player, enemies):
    # Player rest
    print(f'{player.name} takes a short rest at a fire...')
    rest_roll = sum(d8.roll(1))
    rest_heal = player.heal(rest_roll)
    print(f'{player.name} regains {rest_heal}HP.') if rest_heal > 0 \
        else print(f'{player.name} is already at full HP!')
    # Enemy rest loop
    for enemy in enemies:
        if not enemy.defeated:
            rest_roll = sum(d8.roll(1))
            rest_heal = enemy.heal(rest_roll // 2)
            if rest_heal > 0:
                print(f'{enemy.name} took a short rest as well...')
    print()


def fight_loop(d20, d8, enemies, player, fighter, last_location):

    print(f'{player.name} charges at {fighter.name}!!\n')
    combat = 1
    
    while combat:

        combat_cmd = input('What would you like to do? [A]ttack, [R]un away: ')
        if not combat_cmd:
            print("No input detected, please re-enter a command.\n")
            continue
        combat_cmd = combat_cmd.lower().strip()

        if combat_cmd == 'a':
            print('Rolling some dice...\n')
            # no initiative rolls for now, player always goes first...
            # Kirito has the fastest reaction times after all :)

            # player attacks target
            attack_target(d20, d8, fighter, player)  # d20, d8, target, attacker
            enemy_defeated = health_status(player, fighter, 'enemy')
            if enemy_defeated:
                combat = 0

            else:
                # target attacks player
                attack_target(d20, d8, player, fighter)
                player_defeated = health_status(player, fighter, 'player')
                if player_defeated:
                    combat = 0

                else:
                    print(f'{player.name} now has {player.HP}HP')
                    print(f'{fighter.name} now has {fighter.HP}HP\n')
                # time.sleep(1)

        elif combat_cmd == 'r':  # this isn't from DnD reference materials... just needed something
            run_roll = d20.roll(3)
            run_roll.sort()
            run_roll = run_roll[0:2]

            if max(run_roll) >= 10 - player.modifiers[1]:  # DEX modifiers adds to escape chance
                print(f'{player.name} makes a narrow escape to the previous room!\n')
                player.x_location = last_location[1]
                player.y_location = last_location[0]
                combat = 0

            else:
                print(f"{player.name} stumbles and can't get away!\n")
                # target attacks player
                attack_target(d20, d8, player, fighter)
                player_defeated = health_status(player, fighter, 'player')
                if player_defeated:
                    combat = 0

        else:
            print(f"Sorry, the command '{combat_cmd}' wasn't recognized. Please re-enter a command\n")


def attack_target(d20, d8, target, attacker):
    """
    Performs UI output and calls required Combatant methods
    :param d20: A 20 sided Die object
    :param d8: An 8 sided Die object
    :param target: The targeted Combatant object (can be player or fighter)
    :param attacker: The attacker Combatant object (can be player or fighter)
    :return: UI output for combat summary
    """
    roll = sum(d20.roll(1))
    print(f'{attacker.name} rolled a {roll}!')
    hit = attacker.attack(roll, target)
    print(f"{target.name}'s AC is {target.AC}...")

    if hit == 2:
        print(f'{attacker.name} scored a critical hit!!')
        damage_dice = sum(d8.roll(2))  # double rolls for critical
        damage = target.sustain_damage(damage_dice, attacker)
        print(f'{attacker.name} dealt {damage} damage to {target.name}!\n')

    elif hit == 1:
        print(f'{attacker.name} scored a hit!')
        damage_dice = sum(d8.roll(1))
        damage = target.sustain_damage(damage_dice, attacker)
        print(f'{attacker.name} dealt {damage} damage to {target.name}!\n')

    else:
        print(f"{attacker.name}'s attack missed...\n")


def health_status(player, enemy, target):
    """
    Checks the health status of the target
    :param player: The Player object
    :param enemy: The current/attacking enemy Combatant object
    :param target: A string for 'player' or 'enemy' to indicate which health to check
    :return: 0 if target is alive, 1 if target is defeated (related to action required or not)
    """
    if target == 'player':

        if player.HP == 0:
            print(f'{enemy.name} has defeated {player.name}!...')
            print(f'{player.name} awakens at the start of the maze'
                  f', bruised, embarrassed, and barely alive to fight another day...')
            print('* Your health points have been restored to 1 and you have moved to (0, 0) *\n')
            player.x_location = 0 
            player.y_location = 0 
            player.HP = 1
            return 1

        else:
            return 0

    elif target == 'enemy':

        if enemy.HP == 0:
            print(f'{player.name} defeated {enemy.name}!\n')
            enemy.defeated = 1
            return 1

        else:
            return 0
