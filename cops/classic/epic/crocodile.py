from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(crocodile)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class crocodile(Pet):
    icon='🐊'
    description='UwU'
    rarity=0.5
    points=250

    sell = 250
    sacrifice = 250

    health = 3
    physical_attack = 4
    magical_attack = 1
    resistance_physical = 4
    resistance_magical = 4
    intelligent = 3
    weapon_point = 2
