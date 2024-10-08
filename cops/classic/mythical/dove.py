from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(dove)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class dove(Pet):
    icon='🕊️'
    description='hihi'
    rarity=0.4
    points=3000

    sell = 5000
    sacrifice = 3000

    health = 4
    physical_attack = 4
    magical_attack = 1
    resistance_physical = 4
    resistance_magical = 4
    intelligent = 2
    weapon_point = 2
