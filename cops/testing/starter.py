from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(cuoilai)
    gamebase.add_weapon(marble)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class cuoilai(Pet):
    icon='<:cl:1032661892268826675>'
    description='tao thich cuoi day thi sao'
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


class marble(Weapon):
    icon=r"<:marble:952774264900157480>"
    name=r"Hai hon dai"
    information="Nhỏ nhưng nhanh, hai quả trung dai của bạn sẽ được ném đi với tốc độ cao và gây damage cực gắk"

    priority=1

    def on_game_start(self, *a, **kw):
        self.cost = quality_range(200,100,self.quality)
        self.str_damage = quality_range(0.2,0.3,self.quality)
        self.int_damage = quality_range(0.15,0.25,self.quality)
        self.extra_damage = quality_range(0.6,0.77,self.quality)
    
    @property
    def description(self):
        return f"""
Ném 2 viên đá vào 2 kẻ địch bất kì (có thể giống nhau), viên đầu gây {self.str_damage*100:.2f}% STR damage và viên còn lại gây {self.int_damage*100:.2f}% INT damage.
Nếu hai viên trúng một kẻ địch thì đối phương sẽ nhận thêm {self.extra_damage*100:.2f}% INT true damage
Mỗi lần sử dụng mất {self.cost:.2f} WP.
        """.strip()
    
    def active(self):
        if self.pet.weapon_point < self.cost: return
        self.pet.weapon_point -= self.cost

        enemies:list[Pet] = self.game.right.pets if self.pet.team=='left' else self.game.left.pets
        first_enemy:Pet = random.choice(enemies)
        second_enemy:Pet = random.choice(enemies)
        
        first_damage = self.pet.physical_attack*self.str_damage
        self.game.log(f"{self.pet.name} ném viên bi thứ nhất vào {first_enemy.name} và gây {first_damage} damage")
        first_enemy.on_attacked(damage=first_damage, attacker=self.pet, is_true=False, type='physical')

        second_damage = self.pet.intelligent*self.int_damage
        self.game.log(f"{self.pet.name} ném viên bi thứ hai vào {second_enemy.name} và gây {second_damage} damage")
        second_enemy.on_attacked(damage=second_damage, attacker=self.pet, is_true=False, type='physical')
        
        if first_enemy == second_enemy:
            extra = self.pet.intelligent*self.extra_damage
            self.game.log(f"{first_enemy.name} ăn hai bi và mất thêm {extra} damage")
            first_enemy.on_damaged(extra, self.pet, False)
