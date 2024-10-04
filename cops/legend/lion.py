from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(lion)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class lion(Pet):
    icon='<a:lion:1291663541908013147>'
    description='uwu'
    rank='Legend'
    points=10000

    sell = 15000
    sacrifice = 10000

    health = 7
    physical_attack = 7
    magical_attack = 1
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 4
    weapon_point = 1