from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(bear)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class bear(Pet):
    icon='🐻'
    description='có 10% tỉ lệ Gấu giận dữ làm tăng 10% STR trong 2 lượt'
    rank='Epic'
    points=250

    sell = 250
    sacrifice = 250

    health = 4
    physical_attack = 4
    magical_attack = 1
    resistance_physical = 2
    resistance_magical = 2
    intelligent = 3
    weapon_point = 3

    def on_game_start(self):
        self.count = 2
        self.is_angry = 0
        self.init_physical_damage = self.physical_attack

    def active(self):
        if self.is_angry:
            self.count -= 1
        else:
            percent = min(self.level,10) / 100
            if random.uniform(0,1) <= percent:
                self.is_angry = 1
                self.count = 2
                self.physical_attack += self.physical_attack * 10 / 100 
        
        super().active()

        if self.count == 0 and self.is_angry == 1: 
            self.is_angry=0 
            self.physical_attack = self.init_physical_damage