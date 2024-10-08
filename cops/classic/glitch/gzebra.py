from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(gzebra)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class gzebra(Pet):
    aliases=['zebra']
    icon='<a:gzebra:1291681992349585428>'
    description='Không thể bị tấn công bởi STR'
    rarity=0.0005
    points=200000

    sell = 300000
    sacrifice = 200000

    health = 3
    physical_attack = 1
    magical_attack = 5
    resistance_physical = float("inf") # ∞
    resistance_magical = 2
    intelligent = 4
    weapon_point = 8


    def on_game_start(self):
        self.add_event_listener('on_damaged', self.anti_physical_damage)

    def anti_physical_damage(self, damage:float, type:str = None, is_true:bool=False, *a, **kw):
        if is_true: return damage
        if type=='physical': return 0
        return damage
