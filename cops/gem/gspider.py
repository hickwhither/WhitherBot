from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(gspider)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class gspider(Pet):
    aliases=['spider']
    icon='<a:gspider:1291658292480708629>'
    description='uwu'
    rank='Gem'
    points=3000

    sell = 30000
    sacrifice = 20000

    health = 0
    physical_attack = 19
    magical_attack = 0
    resistance_physical = 0
    resistance_magical = 0
    intelligent = 2
    weapon_point = 0
