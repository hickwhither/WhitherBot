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

    health = 8
    strength = 1
    resistance = 5
    intelligent = 1
    weapon_point = 4

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)



