from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hant)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class hant(Pet):
    aliases=['ant']
    icon='🐜'
    description='nhỏ bé nhưng bầy đàn cực mạnh'
    rarity=0.001
    points=500000

    sell = 1000000
    sacrifice = 500000

    health = 4
    physical_attack = 9
    magical_attack = 2
    resistance_physical = 1
    resistance_magical = 1
    intelligent = 4
    weapon_point = 3
