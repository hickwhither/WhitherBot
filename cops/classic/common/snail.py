from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(snail)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class snail(Pet):
    icon='🐌'
    description='Good tank'
    rarity=11.67
    points=1

    sell = 1
    sacrifice = 1

    health = 5
    physical_attack = 1
    magical_attack = 0
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 1
    weapon_point = 3

    def on_game_start(self):
        self.add_event_listener('on_damaged', self.resistance_dmg)

    def resistance_dmg(self, damage:float, type:str = None, is_true:bool=False, *a, **kw):
        if is_true: return damage
        percent = min(self.level,25)/100
        if random.uniform(0, 1) <= percent: return 0
        return damage


