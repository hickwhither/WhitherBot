from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(cuoilai)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class cuoilai(Pet):
    icon='<:cl:1032661892268826675>'
    description='tao thich cuoi day thi sao, may khong cuoi tao va day'
    points=1
    rarity=1
    
    sell=69420
    sacrifice=42069

    health =2
    physical_attack = 2
    magical_attack = 2
    resistance_physical = 2
    resistance_magical = 0
    intelligent =2
    weapon_point =4

    def on_game_start(self):
        self.add_event_listener('on_turn', self.turn)

    def change_name(self, name):
        pos = random.randint(0, len(name)-1)
        name = name[:pos] + self.icon + name[pos:]
        return name

    def turn(self):
        self.game.left.name = self.change_name(self.game.left.name)
        self.game.right.name = self.change_name(self.game.right.name)
        pet:Pet = random.choice(self.game.left.pets + self.game.right.pets)
        pet.name = self.change_name(pet.name)
    
