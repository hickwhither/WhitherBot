from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(feagle)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class feagle(Pet):
    aliases=['eagle']
    icon='<a:eagle:1291676624978448455>'
    description='uwu'
    rarity=0.05
    points=250

    sell = 250000
    sacrifice = 100000

    health = 2
    physical_attack = 13
    magical_attack = 1
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 4
    weapon_point = 1
