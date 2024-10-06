from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(unicorn)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class unicorn(Pet):
    icon='🦄'
    description='hihi'
    rank='Mythical'
    points=3000

    sell = 5000
    sacrifice = 3000

    health = 2
    physical_attack = 1
    magical_attack = 6
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 6
