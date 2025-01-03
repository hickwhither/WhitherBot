from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(ffrog)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class ffrog(Pet):
    aliases=['frog']
    icon='<a:ffrog:1291676580476747786>'
    description='uwu'
    rarity=0.05
    points=250

    sell = 250000
    sacrifice = 100000

    health = 3
    physical_attack = 1
    magical_attack = 10
    resistance_physical = 1
    resistance_magical = 3
    intelligent = 4
    weapon_point = 3
