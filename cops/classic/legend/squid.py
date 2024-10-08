from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(squid)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class squid(Pet):
    icon='<a:squid:1291663546639319040>'
    description='uwu'
    rarity=0.1
    points=10000

    sell = 15000
    sacrifice = 10000

    health = 3
    physical_attack = 1
    magical_attack = 6
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 6
