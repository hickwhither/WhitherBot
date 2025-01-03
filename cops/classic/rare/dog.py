from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(dog)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class dog(Pet):
    icon='🐕'
    description='gâu gâu ẳng ẳng'
    rarity=2
    points=20

    sell = 10
    sacrifice = 10

    health = 4
    physical_attack = 6
    magical_attack = 0
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 4
    weapon_point = 3
