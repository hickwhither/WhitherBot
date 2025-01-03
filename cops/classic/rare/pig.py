from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(pig)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class pig(Pet):
    icon='🐖'
    description='cục khẳng'
    rarity=2
    points=20

    sell = 10
    sacrifice = 10

    health = 4
    physical_attack = 2
    magical_attack = 1
    resistance_physical = 3
    resistance_magical = 4
    intelligent = 1
    weapon_point = 2
