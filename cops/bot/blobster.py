from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(blobster)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class blobster(Pet):
    aliases=['lobster']
    icon='<a:blobster:1291684019997773897>'
    description='wtf trâu thế'
    rank='Bot'
    points = 30000

    sell = 50000
    sacrifice = 10000

    health = 14
    physical_attack = 0
    magical_attack = 0
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 4
    weapon_point = 1
