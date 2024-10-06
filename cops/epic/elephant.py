from game.oop import Pet
from game.oop import Weapon, Effect
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(elephant)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class elephant(Pet):
    icon='🐘'
    description='Loại bỏ debuff (1 lần duy nhất và lần đầu tiên nhận debuff)'
    rank='Epic'
    points=250

    sell = 250
    sacrifice = 250

    health = 5
    physical_attack = 5
    magical_attack = 1
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 2
    weapon_point = 1

    def on_game_start(self):
        self.is_remove_debuff = False
        self.add_event_listener('on_appy_effect', self.remove_debuff)
    
    def remove_debuff(self, type:str="", *args, **kwargs):
        if type == 'debuff' and self.is_remove_debuff==0:
            self.is_remove_debuff = True
            return False
        return True
