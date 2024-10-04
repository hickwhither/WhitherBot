from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(penguin)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class penguin(Pet):
    icon='🐧'
    description='con chim của tao không bay được'
    rank='Epic'
    points=250

    sell = 250
    sacrifice = 250

    health = 2
    physical_attack = 1
    magical_attack = 5
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 2
    weapon_point = 6
