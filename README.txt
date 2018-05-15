# dungeon_crawler
This game is a combination of my previous projects "Combat Game" and "Maze Navigation"
Please see the documention of each for more details

Game consists of three files: 1. bv_dungeon_game.py, 2. dungeon_classes.py, and 3. dungeon_functions.py
1. bv_dungeon_game.py contains all functions and UI output required to run the main game loop
2. dungeon_classes.py is imported as a module and includes classes from prevous projects with modifications as required
3. dungeon_functions.py is imported as a module and includes functions from prevous projects with modifications as required

In brief, the game executes te following:
1. Initialization
2. Game Loop
	a. Commands for move, look around room, check map, check health, rest, and exit
	b. If the palyer moves to a location where an enemy was spawned (static locations for now), combat begins
		- If the enemy is defeated, they will no loonger attack the player on sight, and can not restore health
	c. The player must defeat all enemies and reach the end of the maze to complete the game. 
