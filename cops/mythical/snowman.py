from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(snowman)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class snowman(Pet):
    icon='☃️'
    description='hihi'
    rank='Mythical'
    points=3000

    sell = 5000
    sacrifice = 3000

    health = 3
    physical_attack = 2
    magical_attack = 3
    resistance_physical = 1
    resistance_magical = 2
    intelligent = 2
    weapon_point = 8
