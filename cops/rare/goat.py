from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(goat)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class goat(Pet):
    icon='🐐'
    description='the goaaaat'
    rank='Rare'
    points=20

    sell = 10
    sacrifice = 10

    health = 3
    physical_attack = 2
    magical_attack = 0
    resistance_physical = 2
    resistance_magical = 0
    intelligent = 2
    weapon_point = 2