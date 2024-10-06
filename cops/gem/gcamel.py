from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(gcamel)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class gcamel(Pet):
    aliases=['camel']
    icon='<a:gcamel:1291656048083730492>'
    description='sad'
    rank='Gem'
    points=3000

    sell = 30000
    sacrifice = 20000

    health = 1
    physical_attack = 0
    magical_attack = 14
    resistance_physical = 0
    resistance_magical = 2
    intelligent = 4
    weapon_point = 5
