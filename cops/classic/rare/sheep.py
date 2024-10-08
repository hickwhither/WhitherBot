from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(sheep)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class sheep(Pet):
    icon='🐑'
    description='bê beee'
    rarity=2
    points=20

    sell = 10
    sacrifice = 10

    health = 5
    physical_attack = 1
    magical_attack = 0
    resistance_physical = 2
    resistance_magical = 4
    intelligent = 1
    weapon_point = 3

    def on_game_start(self):
        self.count = 2
        self.is_heal = 0
        self.init_physical_damage = self.physical_attack

    def active(self):
        if self.is_heal:
            self.count -= 1
        else:
            percent = min(self.level,10) / 100
            if random.uniform(0,1) <= percent:
                self.is_heal = 1
                self.count = 2
                self.physical_attack += self.physical_attack * 50 / 100 
        
        super().active()

        if self.count == 0 and self.is_heal == 1: 
            self.is_heal=0 
            self.physical_attack = self.init_physical_damage


