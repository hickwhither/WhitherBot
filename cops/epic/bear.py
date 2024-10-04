from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bear)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class bear(Pet):
    icon='🐻'
    description='Trash'
    rank='Epic'
    points=250

    sell = 250
    sacrifice = 250

    health = 4
    physical_attack = 4
    magical_attack = 1
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 3
