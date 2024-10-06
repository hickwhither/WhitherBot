from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(fox)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class fox(Pet):
    icon='<a:fox:1291663544005296173>'
    description='uwu'
    rank='Legend'
    points=10000

    sell = 15000
    sacrifice = 10000

    health = 4
    physical_attack = 9
    magical_attack = 1
    resistance_physical = 1
    resistance_magical = 2
    intelligent = 4
    weapon_point = 3
