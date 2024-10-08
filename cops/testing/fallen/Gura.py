from game.oop import Pet
from game.oop import Weapon
from game import GameBase, Game

import random

def setup(gamebase: GameBase):
    gamebase.add_pet(GuraRev)
    gamebase.add_weapon(GuraReverseCard)

def quality_range(s, e, q): return s+q*(e-s)

from game.oop import Pet

class GuraRev(Pet):
    aliases=['gura', 'gurarev', 'guragay']
    _icon='<:Gura:1291294067430264875>'
    _icon_holdingcard='<:GuraRev:1291269714110185492>'

    description = 'Gawr Gawr Gawr'
    
    rarity=1
    points = 69420

    sell = 69420
    sacrifice = 42069

    health = 8
    physical_attack = 1
    magical_attack = 1
    resistance_physical = 4
    resistance_magical = 4
    intelligent = 1
    weapon_point = 4

    @property
    def icon(self):
        if not self.weapon: return self._icon
        if self.weapon.id != 'GuraReverseCard': return self._icon
        return self._icon_holdingcard

class GuraReverseCard(Weapon):
    icon=r"<:reversedcardgura:1291310797175259151>"
    information="Gura và Reversed Card?"

    priority = 0


    def on_game_start(self, *a, **kw):
        self.cost = 325

        if self.pet.id == 'GuraRev':
            self.pet.add_event_listener('on_attacked', self.reflect_damage_vjp)
        else:
            self.game.log(f"{self.pet.name} choi saygex")


    @property
    def description(self):
        return f"""
        Vũ khí bị động: Khi bị đối thủ gây dame, Gura sẽ kích hoạt reversed card và hoàn trả lại 50% - 53% và +1% dựa trên level pet cho kẻ tấn công Gura và tiêu tốn 325 WP và không thể bị chặn bởi weapon khác
        """.strip()
    
    def reflect_damage_vjp(self, damage: float, type, attacker: Pet, is_true:bool, *args, **kwargs):

        if self.pet.weapon_point < 325: return
        self.pet.weapon_point -= 325
        
        percent_reflect = (self.pet.level + random.randint(50,53)) / 100
        reflect_damage = damage * percent_reflect

        self.game.log(f"{self.pet.name} phản {reflect_damage} damage lại {attacker.name} và chỉ nhận {damage-reflect_damage} damage")
        attacker.on_damaged(damage=reflect_damage, attacker=attacker, is_true=is_true, type=type)

        return damage-reflect_damage

