from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bgiraff)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class bgiraff(Pet):
    aliases=['giraff']
    icon='<a:bgiraff:1291681985017675828>'
    description='wtf Trâu Thế'
    rarity=0.001
    points = 30000

    sell = 50000
    sacrifice = 10000

    health = 12
    physical_attack = 0
    magical_attack = 0
    resistance_physical = 4
    resistance_magical = 4
    intelligent = 3
    weapon_point = 1
