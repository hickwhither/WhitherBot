from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(deer)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class deer(Pet):
    icon='<a:deer:1291663537671770112> '
    description='uwu'
    rarity=0.1
    points=10000

    sell = 15000
    sacrifice = 10000

    health = 3
    physical_attack = 1
    magical_attack = 11
    resistance_physical = 1
    resistance_magical = 1
    intelligent = 3
    weapon_point = 3
