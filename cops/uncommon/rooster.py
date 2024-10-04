from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(chiken)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class chiken(Pet):
    icon='🐓'
    description='Trash'
    rank='Uncommon'
    points=5

    sell = 2
    sacrifice = 2

    health = 2
    physical_attack = 1
    magical_attack = 0
    resistance_physical = 1
    resistance_magical = 0
    intelligent = 1
    weapon_point = 3
