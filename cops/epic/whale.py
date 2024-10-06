from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(whale)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class whale(Pet):
    icon='🐳'
    description='Tank'
    rank='Epic'
    points=250

    sell = 250
    sacrifice = 250
    
    health = 7
    physical_attack = 1
    magical_attack = 2
    resistance_physical = 3
    resistance_magical = 4
    intelligent = 2
    weapon_point = 1
