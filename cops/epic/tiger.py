from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(tiger)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class tiger(Pet):
    icon='🐅'
    description='Attcker'
    rank='Epic'
    points=250

    sell = 250
    sacrifice = 250

    health = 4
    physical_attack = 6
    magical_attack = 3
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 4
    weapon_point = 1
