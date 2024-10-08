from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(gshrimp)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class gshrimp(Pet):
    aliases=['shrimp']
    icon='<a:gshrimp:1291658286923382848>'
    description='uwu'
    rarity=0.05
    points=3000

    sell = 30000
    sacrifice = 20000

    health = 0
    physical_attack = 0
    magical_attack = 10
    resistance_physical = 0
    resistance_magical = 0
    intelligent = 2
    weapon_point = 10
