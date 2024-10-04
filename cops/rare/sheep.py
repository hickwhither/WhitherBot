from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(sheep)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class sheep(Pet):
    icon='🐑'
    description='bê beee'
    rank='Rare'
    points=20

    sell = 10
    sacrifice = 10

    health = 5
    physical_attack = 1
    magical_attack = 0
    resistance_physical = 2
    resistance_magical = 4
    intelligent = 1
    weapon_point = 3
