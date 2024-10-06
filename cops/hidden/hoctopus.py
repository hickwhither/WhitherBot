from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hoctopus)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class hoctopus(Pet):
    aliases=['octopus']
    icon='<a:hoctopus:1291682005645529138>'
    description='Mực ???'
    rank='Hidden'
    points=500000

    sell = 1000000
    sacrifice = 500000

    health = 3
    physical_attack = 1
    magical_attack = 11
    resistance_physical = 2
    resistance_magical = 3
    intelligent = 1
    weapon_point = 2
