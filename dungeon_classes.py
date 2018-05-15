"""
Contains classes required for "BeardedVagabond's Dungeon Crawler" (bv_dungeon_game.py)
Die: contains roll and stats_rolls methods for various dice rolls in game
Creature: parent class for all combatants in game,
contains attack, sustain_damage, and heal methods for various combat functions
Player: inherits from Creature class, allows for added fight and look methods
"""

import random


# Combat
class Die:

    def __init__(self, sides):
        self.sides = sides

    def __str__(self):
        return f"A {self.sides} sided die."

    def roll(self, rolls):
        """
        rolls n-sided dice a specified number of times
        :param rolls: The number of times to roll the dice
        :return: A list of dice rolls
        """
        return random.sample(range(1, self.sides), rolls)

    def stats_rolls(self):
        """
        This method handles the random stat allocation according to the largest three of a 4d6 roll for each stat
        :return: A list of stats in the following format [STR, DEX, CON, INT, WIS, CHR]
        """
        stats = []
        for i in range(1, 7):
            rolls = self.roll(4)
            rolls.sort()
            rolls = rolls[1:]
            stats.append(sum(rolls))
            random.shuffle(stats)
        return stats


class Combatant:

    def __init__(self, name, stats, x_location=0, y_location=0, defeated=0):
        self.name = name
        self.stats = stats  # reminder: STR, DEX, CON, INT, WIS, CHR
        self.x_location = x_location
        self.y_location = y_location
        self.defeated = defeated

        # Calculates stat modifiers
        modifiers = []
        for i in stats:
            modifiers.append(
                -4 if i in range(2, 4) else
                -3 if i in range(4, 6) else
                -2 if i in range(6, 8) else
                -1 if i in range(8, 10) else
                0 if i in range(10, 12) else
                +1 if i in range(12, 14) else
                +2 if i in range(14, 16) else
                +3 if i in range(16, 18) else
                +4 if i in range(18, 20) else 0)
        self.modifiers = modifiers

        # Calculate armor class assuming leather armor
        self.AC = 11 + self.modifiers[1]

        # Calculate max hit points assuming level 1 rogue (1d8 hit die)
        self.MaxHP = 8 + modifiers[2]
        self.HP = self.MaxHP

    def __str__(self):
        return f"{self.name} with stats of {self.stats}, \n modifiers of {self.modifiers}, \n " \
               f"armor class of {self.AC}, HP of {self.HP}/{self.MaxHP}.\n " \
               f"NOTE: Stats & modifiers are in the format of [STR, DEX, CON, INT, WIS, CHR], \n " \
               f"and at location ({self.x_location}, {self.y_location})"

    def attack(self, d20_roll, enemy):
        """
        Determines if attack is successful
        :param d20_roll: Generated through Die object's roll method
        :param enemy: The object of the targeted fighter
        :return: Integer for hit status - 2 for critical, 1 for hit, 0 for miss
        """
        return 2 if d20_roll == 20 else (1 if d20_roll >= enemy.AC else 0)

    def sustain_damage(self, damage_dice, enemy):  # NOTE: enemy is the attacker, self is damaged target
        """
        Calculates damage according to damage dice + STR modifier and subtracts from HP
        :param damage_dice: The sum of damage dice rolls from Die object's roll method
        :param enemy: The object of the attacking fighter
        :return: Integer for amount of damage sustained from attack (saturated between MaxHP and 0
        """
        damage = damage_dice + enemy.modifiers[0]
        self.HP = min(self.MaxHP, max(0, self.HP - damage))
        return damage

    def heal(self, rest_roll):
        """
        Calculates and applies amount of health restored from short rest
        :param rest_roll: Single dice roll for Die object's roll method
        :return: Integer of amount of health restored
        """
        if self.HP == self.MaxHP:
            rest_heal = 0
        else:
            rest_heal = rest_roll + self.modifiers[2]
            self.HP = min(self.MaxHP, max(0, self.HP + rest_heal))  # saturates HP between MaxHP and 0
        return rest_heal


# Maze Navigation
class Room:
    def __init__(self, doors, size='small', enemy=False):
        self.doors = doors  # 1/0 pseudo-boolean list of [North, East, South, West] openings
        self.size = size  # string for small, medium, large (mainly for future implementation)
        self.enemy = enemy

    def __str__(self):
        openings = []
        if self.doors[0]:
            openings.append('North')

        if self.doors[1]:
            openings.append('East')

        if self.doors[2]:
            openings.append('South')

        if self.doors[3]:
            openings.append('West')
        openings = ', '.join(openings[:-2] + [', and '.join(openings[-2:])])

        return f'The {self.size} room has {openings} doors, and {self.enemy.name}.' if openings and self.enemy else \
            f'The {self.size} room has {openings} doors, and no enemies.' if openings and not self.enemy else \
            f'Empty room!'


# Modified for Dungeon Crawler
class Player(Combatant):

    def move(self, direction, maze_layout):
        """
        Moves the player into a new room if possible
        :param direction: string for north, east, south, west (first letter only)
        :param maze_layout: the maze_layout list housing the full structure
        :return: 1 for successful move, 0 otherwise (NOTE: player will also move location when applicable)
        """

        room = maze_layout[self.y_location][self.x_location]

        if direction == 'n' and room.doors[0]:  # North attempt
            self.y_location -= 1
            return 1

        elif direction == 'e' and room.doors[1]:  # East attempt
            self.x_location += 1
            return 1

        elif direction == 's' and room.doors[2]:  # South attempt
            self.y_location += 1
            return 1

        elif direction == 'w' and room.doors[3]:  # West attempt
            self.x_location -= 1
            return 1

        else:
            compass = 'north' if direction == 'n' else \
                'east' if direction == 'e' else \
                'south' if direction == 's' else 'west'
            print(f'{self.name} walks into a wall when attempting to move {compass}\n')
            return 0

    def look_room(self, room):
        """
        Looks at the current room and lists doors
        :param room: current room object
        :return: UI output
        """

        print(f'{self.name} looks around the room...')
        print(room)

    def check_map(self, maze_choice):
        """
        checks maps to see current location
        :param maze_choice: index of room chosen
        :return: UI output
        """

        print(f'{self.name} checks their map...')
        print(f'Your current coordinates are ({self.x_location}, {self.y_location}) in Maze #{maze_choice+1}.')

    def look_enemies(self, enemies):
        """
        Looks at enemies in field and shows full stats including health
        :param enemies: A list of objects portraying the remaining enemies in the field
        :return: UI output detailed remaining enemies
        """
        for idx, entry in enumerate(enemies):
            print(f'[{idx + 1}] {entry}')

    def fight(self, enemy, enemies):
        """
        Determines if combat can occur with selected enemy index
        :param enemy: Integer index of enemy from field
        :param enemies: A list of objects portraying the remaining enemies in the field
        :return: Integer related to boolean status of combat
        """
        combat = 1 if enemy in range(1, len(enemies) + 1) else 0
        return combat
