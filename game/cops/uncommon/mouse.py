from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(mouse)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class mouse(Pet):
    icon='🐤'
    description='🐁'
    rank='Uncommon'

    sell = 2
    sacrifice = 2

    health = 2
    physical_attack = 0
    magical_attack = 2
    resistance_physical = 1
    resistance_magical = 0
    intelligent = 1
    weapon_point = 2
