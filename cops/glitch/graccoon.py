from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(graccoon)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class graccoon(Pet):
    aliases=['raccoon']
    icon='<a:gzebra:1291681992349585428>'
    description='giựt giựt'
    rank='Glitch'
    points=200000

    sell = 300000
    sacrifice = 200000

    health = 2
    physical_attack = 6
    magical_attack = 6
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 4
    weapon_point = 3
