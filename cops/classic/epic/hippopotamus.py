from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game, Team

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(hippopotamus)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class hippopotamus(Pet):
    icon='🦛'
    description='25% Tỉ lệ đớp 1 phát vào đối thủ mất 70 True Dame (1 lần duy nhất)'
    rarity=0.5
    points=250

    sell = 250
    sacrifice = 250

    health = 5
    physical_attack = 2
    magical_attack = 1
    resistance_physical = 3
    resistance_magical = 3
    intelligent = 3
    weapon_point = 4


    def on_game_start(self):
        self.is_bite = 0
        return super().on_game_start()
    
    def active(self):
        enemies:Team = self.game.left if self.team=='right' else self.game.right
        attack_enemy: Pet = random.choice(enemies.pets)
        if not self.is_bite:
            if random.uniform(0,1) <= 0.25:
                self.is_bite = 1
                attack_enemy.deal_attack(damage=70, is_true=True, type='physical', attacker=self)
            
        return super().active()