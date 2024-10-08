from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hkoala)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class hkoala(Pet):
    aliases=['koala']
    icon='<a:hkoala:1291665379722006550> '
    description='ẩn sâu trong trái tim em'
    rarity=0.001
    points=500000

    sell = 1000000
    sacrifice = 500000

    health = 10
    physical_attack = 1
    magical_attack = 1
    resistance_physical = 4
    resistance_magical = 5
    intelligent = 1
    weapon_point = 1
