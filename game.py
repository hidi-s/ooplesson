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
        self.animals = []


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



class Zoo_Keeper(GameElement):
    IMAGE = "Boy"
    SOLID = True 
    def __init__(self):
        GameElement.__init__(self)

    def interact(self, creature):
        if len(PLAYER.animals) == 0:
            GAME_BOARD.draw_msg("I'm missing my %s! Please help me find him!" %core.level[core.level["lvl"]])
            if core.level[core.level["lvl"]] == "giraffe":
                create_map("map1.txt")
            if core.level[core.level["lvl"]] == "monkey":
                create_map("map2.txt")
        elif len(PLAYER.animals) == 1:
            GAME_BOARD.draw_msg("I see you've found my %s."  %core.level[core.level["lvl"]])
            PLAYER.animals.pop(0) 
            if core.level[core.level["lvl"]] == "giraffe":
                create_map("map1.5.txt")
            core.level["lvl"] += 1 


class Animal(GameElement):
    def __init__(self):
        GameElement.__init__(self)

    def make_noise(self, noise, animal):
        GAME_BOARD.draw_msg("\"%s\", says the %s." % noise, animal)
        pass

    def interact(self, PLAYER):
        # GAME_BOARD.draw_msg("You are almost done. Press \'Enter\' or \'Return\' to place %s back in the pen" % creature)
        # if KEYBOARD[key.ENTER]:            
        #     GAME_BOARD.set_el(PLAYER.x - 1, PLAYER.y, creature)
        PLAYER.animals.append(self)
        GAME_BOARD.draw_msg("You just found our giraffe. Please return him to the baby animal specialist!")

    # def interact(gate)

class Pig(Animal):
    IMAGE = "Pig"
    SOLID = True

    def __init__(self, noise, animal = "pig"):
        self.noise = noise

class Giraffe(Animal):
    IMAGE = "Giraffe"
    SOLID = False

    def __init__(self, noise, animal = "Giraffe"):
        self.noise = noise

class Monkey(Animal):
    IMAGE = "Monkey"
    SOLID = True

    def __init__(self, noise, animal = "Monkey"):
        self.noise = noise 
     
class Banana(GameElement):
    IMAGE = "Banana"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a %s! You have %d %ss!" % (self.name, len(player.inventory), self.name))

class Tofu(Animal):
    pass

class Boundary(GameElement):
    SOLID = True
    def __init__(self, image):
        self.IMAGE = image

class Tree(Boundary):
    IMAGE = "ShortTree"
    def __init__(self):
        pass

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    create_map("map0.txt")

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    # keeper = Zoo_Keeper()
    # GAME_BOARD.register(keeper)
    # GAME_BOARD.set_el(11, 3, keeper)

    GAME_BOARD.draw_msg("I wonder what happens if I talk to someone. I see a baby animal specialist over there! He looks worried....")

    # giraffe = Giraffe("beh")
    # GAME_BOARD.register(giraffe)
    # GAME_BOARD.set_el(5,5, giraffe)

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
    # if KEYBOARD[key.R]:
    #     pass

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

def create_map(textfile):
    map_positions = []

    map0 = open(textfile)
    rows = map0.read().split("\n")
    for line in rows:
        items = line.split(" ")
        map_positions.append(items)
    for x in range(len(items)):
        for y in range(len(rows)):
            # print map_positions[y]
            if ord(map_positions[y][x]) == ord("R"):
                rock = Rock()
                GAME_BOARD.register(rock)
                GAME_BOARD.set_el(x, y, rock)
                print rock
            elif ord(map_positions[y][x]) == ord("P"): 
                pen = Boundary("Pen")
                GAME_BOARD.register(pen)
                GAME_BOARD.set_el(x, y, pen)
                print pen
            elif ord(map_positions[y][x]) == ord("Z"):
                keeper = Zoo_Keeper()
                GAME_BOARD.register(keeper)
                GAME_BOARD.set_el(x, y, keeper)
            elif ord(map_positions[y][x]) == ord("G"):
                giraffe = Giraffe("Beh!")
                GAME_BOARD.register(giraffe)
                GAME_BOARD.set_el(x, y, giraffe)
            elif ord(map_positions[y][x]) == ord("-") or ord(map_positions[y][x]) == ord("|"):
                wall = Boundary("Wall")
                GAME_BOARD.register(wall)
                GAME_BOARD.set_el(x, y, wall)
            elif ord(map_positions[y][x]) == ord("B"):
                banana = Banana()
                GAME_BOARD.register(banana)
                GAME_BOARD.set_el(x, y, banana)
            elif ord(map_positions[y][x]) == ord("M"):
                monkey = Monkey("eeek! eeek!")
                GAME_BOARD.register(monkey)
                GAME_BOARD.set_el(x, y, monkey)
            elif ord(map_positions[y][x]) == ord("T"):
                tree = Tree()
                GAME_BOARD.register(tree)
                GAME_BOARD.set_el(x, y, tree)
            # elif ord(map_positions[y][x]) == ord("."):
            #     PLAYER = Character()
            #     GAME_BOARD.register(PLAYER)
            #     GAME_BOARD.set_el(PLAYER.x, PLAYER.y, PLAYER)
    # global PLAYER
    # GAME_BOARD.register(PLAYER)
    # GAME_BOARD.set_el(PLAYER.x, PLAYER.y, PLAYER)