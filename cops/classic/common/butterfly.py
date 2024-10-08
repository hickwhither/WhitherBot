from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(butterfly)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class butterfly(Pet):
    icon='🦋'
    description='Hai bàn tay của em như hai con bướm xinh xinh'
    rarity=11.67
    points=1

    sell = 1
    sacrifice = 1

    health = 1
    physical_attack = 1
    magical_attack = 0
    resistance_physical = 0
    resistance_magical = 0
    intelligent = 1
    weapon_point = 2
