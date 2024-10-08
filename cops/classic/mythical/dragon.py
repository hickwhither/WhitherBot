from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(dragon)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class dragon(Pet):
    icon='🐉'
    description='Trash'
    rarity=0.4
    points=3000

    sell = 5000
    sacrifice = 3000

    health = 4
    physical_attack = 2
    magical_attack = 5
    resistance_physical = 2
    resistance_magical = 3
    intelligent = 4
    weapon_point = 5
