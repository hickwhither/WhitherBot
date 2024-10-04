from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(badger)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class badger(Pet):
    icon='🦡'
    description='Nhìn giống chồn nhưng không phải chồn, nhưng thực chất là họ chồn'
    rank='Rare'
    points=20

    sell = 5
    sacrifice = 5

    health = 3
    physical_attack = 1
    magical_attack = 3
    resistance_physical = 1
    resistance_magical = 3
    intelligent = 2
    weapon_point = 2
