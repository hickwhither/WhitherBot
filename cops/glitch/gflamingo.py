from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(gflamingo)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class gflamingo(Pet):
    aliases=['flamingo']
    icon='<a:gflamingo:1291681979024150529>'
    description='giựt giựt'
    rank='Glitch'
    points=200000

    sell = 300000
    sacrifice = 200000

    health = 3
    physical_attack = 9
    magical_attack = 1
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 4
    weapon_point = 4
