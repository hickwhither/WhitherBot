from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(owl)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class owl(Pet):
    icon='<a:owl:1291663550045224980>'
    description='uwu'
    rarity=0.1
    points=10000

    sell = 15000
    sacrifice = 10000

    health = 10
    physical_attack = 1
    magical_attack = 2
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 4
    weapon_point = 1
