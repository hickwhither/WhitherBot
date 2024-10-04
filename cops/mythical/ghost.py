from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(ghost)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class ghost(Pet):
    icon='👻'
    description='Không thể bị tấn công bởi vật lý'
    rank='Mythical'
    points=3000

    sell = 5000
    sacrifice = 3000

    health = 6
    physical_attack = 0
    magical_attack = 5
    resistance_physical = 999
    resistance_magical = 1
    intelligent = 2
    weapon_point = 6
