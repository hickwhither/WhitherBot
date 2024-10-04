from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bhedge)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class bhedge(Pet):
    aliases=['hedge']
    icon='<a:bhedge:1291681994861707346>'
    description='wtf Trâu Thế'
    rank='Bot'
    points = 30000

    sell = 50000
    sacrifice = 10000

    health = 7
    physical_attack = 0
    magical_attack = 0
    resistance_physical = 6
    resistance_magical = 6
    intelligent = 4
    weapon_point = 2
