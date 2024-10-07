from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(gpanda)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class gpanda(Pet):
    aliases=['panda']
    icon='<a:gpanda:1291657829371084810>'
    description='uwu'
    rank='Gem'
    points=3000

    sell = 30000
    sacrifice = 20000

    health = 1
    physical_attack = 10
    magical_attack = 0
    resistance_physical = 0
    resistance_magical = 0
    intelligent = 4
    weapon_point = 9
