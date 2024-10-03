from game.pet import Pet
from game.weapon import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(cuoilai)
    gamebase.add_weapon(marble)

def quality_range(s, e, q): return s+q*(e-s)

from game.pet import Pet

class cuoilai(Pet):
    icon='<:cl:1032661892268826675>'
    description='tao thich cuoi day thi sao'
    
    sell=69420
    sacrifice=42069

    health =1
    strength =2
    resistance =3
    intelligent =4
    weapon_point =5

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
    
    def active(self):
        enemies:list[Pet] = self.game.right if self.team=='left' else self.game.left
        enemy_attack = random.choice(enemies)
        enemy_attack.on_attacked(self.strength, self, False)


class marble(Weapon):
    icon=r"<:marble:952774264900157480>"
    info="Nhỏ nhưng nhanh, hai quả trung dai của bạn sẽ được ném đi với tốc độ cao và gây damage cực gắk"
    description=r"""
Ném 2 viên đá vào 2 kẻ địch bất kì, viên đầu gây 85-105% STR damage và viên còn lại gây 80-100% INT damage.
Nếu hai viên trúng một kẻ địch thì đối phương sẽ nhận thêm 20-30% INT true damage
Mỗi lần sử dụng mất 100-200 WP.
    """.strip()

    priority=1

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.cost = quality_range(100,200,self.quality)
        self.str_damage = quality_range(0.85,1.05,self.quality)
        self.int_damage = quality_range(0.8,1,self.quality)
        self.extra_damage = quality_range(0.2,0.3,self.quality)

    def description_specific(self):
        return f"""
Ném 2 viên đá vào 2 kẻ địch bất kì (có thể giống nhau), viên đầu gây {self.str_damage*100:.2f}% STR damage và viên còn lại gây {self.int_damage*100:.2f}% INT damage.
Nếu hai viên trúng một kẻ địch thì đối phương sẽ nhận thêm {self.extra_damage*100:.2f}% INT true damage
Mỗi lần sử dụng mất {self.cost:.2f} WP.
        """.strip()
