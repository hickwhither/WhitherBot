from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hsnake)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class hsnake(Pet):
    aliases=['snake']
    icon='<a:hsnake:1291682011571945493>'
    description='Rắn nè'
    rank='Hidden'
    points=500000

    sell = 1000000
    sacrifice = 500000

    health = 2
    physical_attack = 13
    magical_attack = 1
    resistance_physical = 3
    resistance_magical = 2
    intelligent = 3
    weapon_point = 1
