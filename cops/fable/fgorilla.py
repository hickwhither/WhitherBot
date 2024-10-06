from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(fgorilla)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class fgorilla(Pet):
    aliases=['gorilla']
    icon='<a:fgorilla:1291676577830014996>'
    description='uwu'
    rank='Fable'
    points=250

    sell = 250000
    sacrifice = 100000

    health = 8
    physical_attack = 7
    magical_attack = 1
    resistance_physical = 2
    resistance_magical = 3
    intelligent = 4
    weapon_point = 1
