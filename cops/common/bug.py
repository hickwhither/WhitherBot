from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bug)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class bug(Pet):
    icon='🐛'
    description='Trash'
    rank='Common'
    points=1

    sell = 1
    sacrifice = 1

    health = 1
    physical_attack = 0
    magical_attack = 1
    resistance_physical = 0
    resistance_magical = 0
    intelligent = 1
    weapon_point = 2
