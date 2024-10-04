from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bsloth)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class bsloth(Pet):
    aliases=['sloth']
    icon='<a:bsloth:1291684339956056065>'
    description='wtf Trâu Thế'
    rank='Bot'
    points = 30000

    sell = 50000
    sacrifice = 10000

    health = 9
    physical_attack = 0
    magical_attack = 0
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 8
