from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(fboar)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class fboar(Pet):
    aliases=['boar']
    icon='<a:fboar:1291676627876446218>'
    description='uwu'
    rank='Fable'
    points=250

    sell = 250000
    sacrifice = 100000

    health = 7
    physical_attack = 5
    magical_attack = 1
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 4
    weapon_point = 4