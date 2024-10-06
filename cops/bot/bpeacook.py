from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bpeacook)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class bpeacook(Pet):
    aliases=['peacook']
    icon='<a:bpeacock:1292326994016604274>'
    description='wtf Trâu Thế'
    rank='Bot'
    points = 30000

    sell = 50000
    sacrifice = 10000

    health = 10
    physical_attack = 0
    magical_attack = 0
    resistance_physical = 5
    resistance_magical = 5
    intelligent = 3
    weapon_point = 6
