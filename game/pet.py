from __future__ import annotations
from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from game import Game
#     from game.weapon import Weapon
class Game:...
class Weapon:...
from typing import Callable
import random

class Pet:
    """
    ## Input Pramaters
    - `icon`: icon của pet emoji -> `str`
    - `description`: mô tả kỹ năng -> `str`
    - `rank`: Rank của bé -> `str` : Common, Uncommon, Rare, Epic, Mythical, Gem, Legend, Fable, Bot, Hiden, Glitch, Fallen
    
    - Thông số cơ bản: `health`, `physical_attack`, `resistance_physical`, `intelligent`, `weapon_point` -> `int`
    - `sell`: nhận được khi sell
    - `sacrifice`: nhận được khi sacrifice

    - `active`: gọi khi đến lượt (đánh thường)
    - `calculate_level`: tính lại các thông số dựa theo level

    ## Built-in Pramaters
    - `game`: class Game
    - `name`: tên -> `str`
    - `level`: cấp độ -> `int`
    - `weapon`: vũ khí -> `Weapon`
    - `team`: "left"/"right" -> `str`
    - `health`, `physical_attack`, `magical_attack`, `resistance_physical`, `resistance_magical`, `intelligent`, `weapon_point` sẽ được tính lại bằng super().__init__() dựa trên level


    ## Events
    - `on_attacked`: bị tấn công
    - `on_heal`: được hồi máu
    - `on_wp_replenish`: được hồi WP

    ## Add event listener(name, func)
    - `on_attack`: bị tấn công, (damage, attacker, is_true) và trả về damage nếu có đổi giá trị
    - `on_damaged`: bị sát thương, (damage, is_true) và trả về damage nếu có đổi giá trị
    - `on_healed`: được hồi máu, (health) và trả về health nếu có đổi giá trị
    - `on_wp_replenished`: được hồi wp, (wp) và trả về wp nếu có đổi giá trị
    """
    icon: str
    information: str
    description: str
    rank: str

    sell: int
    sacrifice: int

    health: int # HP
    physical_attack: int # STR
    magical_attack: int
    resistance_physical: int # RES
    resistance_magical: int 
    intelligent: int # INT
    weapon_point: int # WP

    active: Callable

    max_health: int
    max_wp: int

    game: Game
    name: str
    level: int
    weapon: Weapon
    team: str # left/right

    events: dict[list[Callable]]

    def __init__(self, param:dict):
        self.param = param
        
        self.id = param.get('id')
        self.name = param.get('name') or self.__class__.__name__
        self.level = param['level']
        
        self.calculate_level()
    
    
    def calculate_level(self):
        self.health = self.health * self.level * 2 + 500
        self.physical_attack = self.physical_attack * self.level + 100
        self.magical_attack = self.physical_attack * self.level + 100
        self.resistance_physical = self.resistance_physical * self.level * 2 + 100
        self.resistance_magical = self.resistance_magical * self.level * 2 + 100
        self.intelligent = self.intelligent * self.level + 100
        self.weapon_point = self.weapon_point * self.level * 2 + 500
        self.max_health = self.health
        self.max_wp = self.weapon_point
    
    def on_game_start(self): pass
    def start_game(self, weapon:Weapon=None, game:Game=None, team:str=None):
        self.game = game
        self.team = team
        self.weapon = weapon
        self.events = {}
        self.on_game_start()


    def active(self):
        enemies: list[Pet] = self.game.right.pets if self.team=='left' else self.game.left.pets
        enemy_attack = random.choice(enemies)

        self.game.log(f"{self.name} đã tấn công {enemy_attack.name} và gây {self.physical_attack} damage")
        enemy_attack.on_attacked(self.physical_attack, self, False)
    
    
    @property
    def status(self):
        return {
            'id': self.id,
            'icon': self.icon,
            'name': self.name,
            'level': self.level,
            'weapon': self.weapon.id if self.weapon else None,
            'pramaters':{
                'health': self.health,
                'physical_attack': self.physical_attack,
                'magical_attack': self.magical_attack,
                'resistance_physical': self.resistance_physical,
                'resistance_magical': self.resistance_physical,
                'intelligent': self.intelligent,
                'weapon_point': self.weapon_point,
                'max_health': self.max_health,
                'max_wp': self.max_wp,
            }
        }



    # Pet
    def add_event_listener(self, name:str, func:Callable, *args, **kwargs):
        if not self.events.get(name): self.events[name] = []
        self.events[name].append(func, *args, **kwargs)
    

    def on_attacked(self, damage:float, type:str, attacker:Pet, is_true:bool=False, *args, **kwargs):
        
        self.game.indent_log += 1
        for func in self.events.get('on_attacked') or []:
            damage = func(damage, type, attacker, is_true, *args, **kwargs) or damage
        self.game.indent_log -= 1
        
        self.on_damaged(damage, type, is_true)

    def on_damaged(self, damage:float, type:str = None, is_true:bool=False, *args, **kwargs):
        
        self.game.indent_log += 1
        for func in self.events.get('on_damaged') or []:
            damage = func(damage, type, is_true, *args, **kwargs) or damage
        self.game.indent_log -= 1
        
        if not is_true: 
            if type == "physical": damage -= 0.8 * ( (25 + 2 * self.level * self.resistance_physical) / (125 + 2 * self.level * self.resistance_physical) )
            else: damage -= 0.8 * ( (25 + 2 * self.level * self.resistance_physical) / (125 + 2 * self.level * self.resistance_magical) )
        damage = max(0, damage)
        self.health -= damage
        self.health = max(self.health, 0)
    
    def on_healed(self, h: float, *args, **kwargs):
        
        self.game.indent_log += 1
        for func in self.events.get('on_healed') or []:
            damage = func(h, *args, **kwargs) or damage
        self.game.indent_log -= 1

        self.health += h
        self.health = min(self.health, self.max_health)
    
    def on_wp_replenished(self, wp, *args, **kwargs):

        self.game.indent_log += 1
        for func in self.events.get('on_damaged') or []:
            damage = func(wp, *args, **kwargs) or damage
        self.game.indent_log -= 1

        self.weapon_point += wp
        self.weapon_point = min(self.health, self.max_wp)



