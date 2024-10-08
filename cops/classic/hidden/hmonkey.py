from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hmonkey)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class hmonkey(Pet):
    aliases=['monkey']
    icon='<a:hmonkey:1291682003296714753>'
    description='Hua Hua Hua Ha Ha Ha'
    rarity=0.001
    points=500000

    sell = 1000000
    sacrifice = 500000

    health = 3
    physical_attack = 7
    magical_attack = 7
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 1
