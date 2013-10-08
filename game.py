import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 14
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True 

class Character(GameElement):
    IMAGE = "Girl"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []


    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def talk(self, player, other):
        pass


class Animal(GameElement):
    def __init__(self):
        GameElement.__init__(self)

    def make_noise(self, noise, animal):
        GAME_BOARD.draw_msg("\"%s\", says the %s." % noise, animal)
        pass

class Pig(Animal):
    IMAGE = "Pig"
    SOLID = True

    def __init__(self, noise, animal = "pig"):
        self.noise = noise

class Giraffe(Animal):
    IMAGE = "Pig"
    SOLID = True

    def __init__(self, noise, animal = "pig"):
        self.noise = noise

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just found our giraffe. Please return him to the baby animal specialist!")

class Tofu(Animal):
    pass

class Boundary(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    # rock = Rock()
    # GAME_BOARD.register(rock)
    # GAME_BOARD.set_el(2, 1, rock) #starts at top left, goes right first, then down
    # print "The rock is at", (rock.x, rock.y)


    for i in range(14):
        wall = Boundary()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(i, 0, wall)
        GAME_BOARD.set_el(i, 9, wall)
    for i in range(10):
        wall = Boundary()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(0, i, wall)
        GAME_BOARD.set_el(13, i, wall)



    rock_positions = [
            (2,1),
            (1,2),
            (3,2),
            (2,3)
        ]
    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False
    
    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game is wicked awesome.")
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    giraffe = Giraffe("beh")
    GAME_BOARD.register(giraffe)
    GAME_BOARD.set_el(5,5, giraffe)

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction: 
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)