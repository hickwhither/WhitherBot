from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(snail)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class snail(Pet):
    icon='🐌'
    description='Good tank'
    rank='Common'

    sell = 1
    sacrifice = 1

    health = 5
    physical_attack = 1
    magical_attack = 0
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 1
    weapon_point = 3
