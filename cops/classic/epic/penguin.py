from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(penguin)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class penguin(Pet):
    icon='🐧'
    description='10% tỉ lệ đỡ được damage'
    rarity=0.5
    points=250

    sell = 250
    sacrifice = 250

    health = 2
    physical_attack = 1
    magical_attack = 5
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 2
    weapon_point = 6

    def on_game_start(self):
        self.add_event_listener('on_damage', self.reflect_dame)
    
    def reflect_dame(self, damage:float, type:str = None, is_true:bool=False, *a, **kw,):
        if is_true: return damage
        if random.uniform(0,1) <= 0.1:
            return 0
        return damage
