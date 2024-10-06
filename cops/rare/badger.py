from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game, Team

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(badger)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class badger(Pet):
    icon='🦡'
    description='Nhìn giống chồn nhưng không phải chồn, nhưng thực chất là họ chồn'
    rank='Rare'
    points=20

    sell = 5
    sacrifice = 5

    health = 3
    physical_attack = 1
    magical_attack = 3
    resistance_physical = 1
    resistance_magical = 3
    intelligent = 2
    weapon_point = 2

    def on_game_start(self):
        self.count = 3
        return super().on_game_start()
    
    def active(self):
        enemies:Team = self.game.left if self.team=='right' else self.game.right
        self.count -= 1
        
        if self.count == 0:
            self.count = 3
            for e in enemies.pets:
                e: Pet
                e.on_damaged(damage=2*self.health, type='physical')
        
        return super().active()
    



