"""
A combination of previous projects...
A text-based dungeon crawler in which hte player navigates a maze and must defeat enemies to progress
"""

import dungeon_classes as dc
import dungeon_functions as dfunc


def print_header():
    print('=============================================')
    print()
    print("     BeardedVagabond's Dungeon Crawler")
    print()
    print('=============================================')
    print()


def initialize():
    """
    Creates all required objects for game function
    :return: maze_choice, maze_layout, d20, d8, enemies, player
    """
    # initialize_combatants
    d6 = dc.Die(6)
    d8 = dc.Die(8)
    d20 = dc.Die(20)

    enemies = [
        dc.Combatant('Heathcliffe', d6.stats_rolls()),
        dc.Combatant('Oberon', d6.stats_rolls()),
        dc.Combatant('Death Gun', d6.stats_rolls()),
    ]

    # verify player name input
    player_name = ''
    while not player_name:

        player_name = input('What is your name? ')  # input "Kirito" for thematic continuity

        if not player_name:
            print('Input not recognized. Please re-enter a name.\n')
    player = dc.Player(player_name, d6.stats_rolls())

    print('A heroic adventurer wanders into a maze...')
    print(player)

    # Create mazes
    maze_choice, maze_layout = dfunc.maze_initialization()
    enemy_locations = spawn_enemies(enemies, maze_choice)

    return maze_choice, maze_layout, d20, d8, enemies, enemy_locations, player


def spawn_enemies(enemies, maze_choice):
    """
    Chooses enemies in order to spawn at preset locations for each map
    :param enemies: A list of enemies in the field
    :param maze_choice: int index of which maze was chosen
    :return: N/A
    """
    spawn_rooms = [[], [], []]
    if maze_choice == 0:
        spawn_rooms[0] = [3, 1]  # x, y
        spawn_rooms[1] = [2, 3]  # x, y
        spawn_rooms[2] = [5, 6]  # x, y
    elif maze_choice == 1:
        spawn_rooms[0] = [4, 3]  # x, y
        spawn_rooms[1] = [7, 6]  # x, y
        spawn_rooms[2] = [7, 1]  # x, y
    elif maze_choice == 2:
        spawn_rooms[0] = [2, 1]  # x, y
        spawn_rooms[1] = [5, 3]  # x, y
        spawn_rooms[2] = [0, 2]  # x, y

    enemies[0].x_location = spawn_rooms[0][0]
    enemies[0].y_location = spawn_rooms[0][1]

    enemies[1].x_location = spawn_rooms[1][0]
    enemies[1].y_location = spawn_rooms[1][1]

    enemies[2].x_location = spawn_rooms[2][0]
    enemies[2].y_location = spawn_rooms[2][1]

    return spawn_rooms


def game_loop(maze_choice, maze_layout, d20, d8, enemies, enemy_locations, player):
    """
    Executes the main game loop
    :param maze_choice: int index of which maze was chosen
    :param maze_layout: list describing the layout of the maze rooms
    :param player: Player object with inputted name
    :param d20: A 20 sided Die object
    :param d8: An 8 sided Die object
    :param enemies: A list of enemies in the field
    :return: N/A
    """
    while True:

        # Check for undefeated enemy in room
        player_location = [player.x_location, player.y_location]
        if player_location == enemy_locations[0]:
            fighter = enemies[0]
            if fighter.defeated:
                pass
            else:
                print(f'{player.name} spots an enemy in the room and charges at {fighter.name}!')
                dfunc.fight_loop(d20, d8, enemies, player, fighter, last_location)
        elif player_location == enemy_locations[1]:
            fighter = enemies[1]
            if fighter.defeated:
                pass
            else:
                print(f'{player.name} spots an enemy in the room and charges at {fighter.name}!')
                dfunc.fight_loop(d20, d8, enemies, player, fighter, last_location)
        elif player_location == enemy_locations[2]:
            fighter = enemies[2]
            if fighter.defeated:
                pass
            else:
                print(f'{player.name} spots an enemy in the room and charges at {fighter.name}!')
                dfunc.fight_loop(d20, d8, enemies, player, fighter, last_location)

        cmd = input('Do you wish to [M]ove, [L]ook around room, [C]heck map, Check [h]ealth, [R]est, or E[x]it? ')
        if not cmd:
            print("No input detected, please re-enter a command\n")
            continue

        cmd = cmd.lower().strip()

        if cmd == 'm':
            move = 0
            # Record last location
            last_location = [player.y_location, player.x_location]

            while not move:
                move = dfunc.move_loop(maze_layout, move, player)

        elif cmd == 'l':
            player.look_room(maze_layout[player.y_location][player.x_location])
            print()

        elif cmd == 'c':
            player.check_map(maze_choice)
            print()

        elif cmd == 'h':
            print(f'{player.name} currently has {player.HP}/{player.MaxHP}HP.\n')

        elif cmd == 'r':
            dfunc.rest(d8, player, enemies)

        elif cmd == 'x':
            print('Thanks for playing!')
            break

        else:
            print(f"I'm sorry, {cmd} was not recognized. Please re-enter a command.\n")

        # Set and check end of game conditions
        x_finish = 6 if maze_choice == 0 else 7 if maze_choice == 1 else 0
        y_finish = 6 if maze_choice == 0 else 0 if maze_choice == 1 else 1
        enemies_defeated = [enemies[0].defeated, enemies[1].defeated, enemies[2].defeated]

        if player.x_location == x_finish and player.y_location == y_finish and all(enemies_defeated):
            print(f'{player.name} has made it to the end of the maze and defeated all enemies! Congratulations!!')
            print("'Thanks for playing!")
            break
        elif player.x_location == x_finish and player.y_location == y_finish and not all(enemies_defeated):
            print(f"{player.name} has made it to the end of the maze... but enemies remain and the exit won't open...")


def main():
    print_header()
    maze_choice, maze_layout, d20, d8, enemies, enemy_locations, player = initialize()
    game_loop(maze_choice, maze_layout, d20, d8, enemies, enemy_locations, player)


if __name__ == '__main__':
    main()
