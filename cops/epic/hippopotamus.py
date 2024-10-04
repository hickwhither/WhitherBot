from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hippopotamus)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class hippopotamus(Pet):
    icon='🦛'
    description='Trash'
    rank='Epic'
    points=250

    sell = 250
    sacrifice = 250

    health = 5
    physical_attack = 2
    magical_attack = 1
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 3
    weapon_point = 4
