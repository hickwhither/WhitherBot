from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hlizard)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class hlizard(Pet):
    aliases=['lizard']
    icon='<a:hlizard:1291681997600722965>'
    description='Biến Mất Tiêu?'
    rank='Hidden'
    points=500000

    sell = 1000000
    sacrifice = 500000

    health = 2
    physical_attack = 1
    magical_attack = 13
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 2
