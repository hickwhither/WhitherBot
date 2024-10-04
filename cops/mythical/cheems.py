from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(cheems)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class cheems(Pet):
    icon='<:cheems:926731856693583892>'
    description='sad'
    rank='Mythical'
    points=3000

    sell = 5000
    sacrifice = 3000

    health = 4
    physical_attack = 5
    magical_attack = 5
    resistance_physical = 3
    resistance_magical = 2
    intelligent = 4
    weapon_point = 4