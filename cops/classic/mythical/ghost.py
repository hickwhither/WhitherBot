from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(ghost)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class ghost(Pet):
    icon='👻'
    description='Không thể bị tấn công bởi STR'
    rarity=0.4
    points=3000

    sell = 5000
    sacrifice = 3000

    health = 6
    physical_attack = 0
    magical_attack = 5
    resistance_physical = float("inf") # ∞
    resistance_magical = 1
    intelligent = 4
    weapon_point = 6

    def on_game_start(self):
        self.add_event_listener('on_damaged', self.anti_physical_damage)

    def anti_physical_damage(self, damage:float, type:str = None, is_true:bool=False, *a, **kw):
        if is_true: return damage
        if type=='physical': return 0
        return damage
    
    def active(self):
        enemies: list[Pet] = self.game.right.pets if self.team=='left' else self.game.left.pets
        enemy_attack = random.choice(enemies)

        self.game.log(f"{self.name} đã tấn công {enemy_attack.name} và gây {self.magical_attack} damage")
        enemy_attack.on_attacked(damage=self.magical_attack, type="magical", attacker=self, is_true=False)
