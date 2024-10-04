from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(gparrot)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class gparrot(Pet):
    aliases=['parrot']
    icon='<a:gparrot:1291681988608135188>'
    description='giựt giựt'
    rank='Glitch'
    points=200000

    sell = 300000
    sacrifice = 200000

    health = 8
    physical_attack = 1
    magical_attack = 1
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 4
    weapon_point = 5
