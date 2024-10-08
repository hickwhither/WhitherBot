from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bdino)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class bdino(Pet):
    aliases=['dino']
    icon='<a:bdino:1291691491529461811>'
    description='wtf Trâu Thế'
    rarity=0.001
    points = 30000

    sell = 50000
    sacrifice = 10000

    health = 13
    physical_attack = 0
    magical_attack = 0
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 4
