from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(cat)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class cat(Pet):
    icon='🐈'
    description='con meo de thw pho mai que cute'
    rank='Rare'
    points=20

    sell = 10
    sacrifice = 10

    health = 3
    physical_attack = 1
    magical_attack = 2
    resistance_physical = 1
    resistance_magical = 3
    intelligent = 2
    weapon_point = 6
