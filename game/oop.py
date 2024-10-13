from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Game

from typing import Callable
import random


levels = [
    (100, 10),
    (500, 10), 
    (1000, 10), 
    (5000, 10), 
    (10000, 10), 
    (40000, 25), 
    (70000, 5), 
    (100000, 15), 
    (500000, 5) 
]

def next_xp(level):
    sum = 0
    for increment, level_count in levels:
        
        if level < level_count:
            return sum+level*increment
        sum += increment*level_count
    return float('inf')

def calculate_level(xp):
    sum = 0
    for increment, level_count in levels:
        threshold = increment*level_count
        if xp < threshold:
            return sum + xp // increment + 1
        xp -= threshold
        sum += level_count

    return 100


class Pet:
    """
    ## Input Pramaters
    - `aliases`: cách gọi khác -> `list[str] / Iterable[str]`
    - `icon`: icon của pet emoji -> `str`
    - `description`: mô tả kỹ năng -> `str`
    - `rarity`: độ hiếm -> `float`
    
    - Thông số cơ bản: `health`, `physical_attack`, `resistance_physical`, `intelligent`, `weapon_point` -> `int`
    - `points`: giá trị pet
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

    ## Actions
    - `deal_attack`: tấn công pet này (damage, type, attacker, is_true) (gọi on_attacked)
    - `deal_damage`: game damage lên pet này nhưng không có attacker (damage, type, is_true) (gọi on_damaged)
    - `apply_effect`: gây hiệu ứng lên pet này (id) (gọi on_apply_effect)

    ## Add event listener(name, func)
    - `on_turn`: khi tới lượt bản thân đi, trả về (skip_active) tức là bị bỏ lượt
    - `on_appy_effect`: bị dính hiệu ứng (effectid, type('buff'/'debuff')) trả về True/False nếu hiệu ứng có hiệu
    - `on_attacked`: bị tấn công, (damage, type, attacker, is_true) và trả về damage nếu có đổi giá trị
    - `on_damaged`: bị sát thương, (damage, type, is_true) và trả về damage nếu có đổi giá trị (type là physical/magical)
    - `on_healed`: được hồi máu, (health) và trả về health nếu có đổi giá trị
    - `on_wp_replenished`: được hồi wp, (wp) và trả về wp nếu có đổi giá trị
    """
    aliases: list[str]
    icon: str
    information: str
    description: str
    rank: str # Shouldn't be touch
    rarity: float
    points: int
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
    effects: list[Effect]

    def __init__(self, param:dict={}):
        self.param = param
        
        self.id = param.get('id')
        self.name = param.get('name') or self.__class__.__name__
        self.xp = param.get('xp') or 0
        self.level = calculate_level(self.xp)
        self.weapon = None
    

    # Game start
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
        self.calculate_level()
        self.game = game
        self.team = team
        self.weapon = weapon
        self.events = {}
        self.effects = []
        self.on_game_start()


    # Actions
    def deal_attack(self, damage:float, type:str, attacker:Pet, is_true:bool=False, *a, **kw): self.on_attacked(damage, type, attacker, is_true, *a, **kw)
    def deal_damage(self, damage:float, type:str=None, is_true:bool=False, *a, **kw): self.on_damaged(damage, type, is_true, *a, **kw)
    def apply_effect(self, effectid:str, *a, **kw): self.on_apply_effect(effectid, *a, **kw)
    

    # Events
    def add_event_listener(self, name:str, func:Callable, *args, **kwargs):
        if not self.events.get(name): self.events[name] = []
        self.events[name].append(func, *args, **kwargs)
    
    def on_turn(self):
        skip_active = False

        self.effects = filter(lambda x: x.is_alive, self.effects)

        for effect in self.effects:
            if effect.is_alive == False: continue
            sa = effect.on_turn() or False
            skip_active = sa or skip_active
        
        for func in self.events.get('on_turn') or []:
            sa = func() or False
            skip_active = sa or skip_active
    
        if not skip_active: self.active()

    def on_apply_effect(self, effectid:str, *args, **kwargs):
        allow_to_apply = True
        effect_cls = self.game.gamebase.effects.get(effectid)
        effect: Effect = effect_cls(self, *args, **kwargs)

        self.game.indent_log += 1
        for effect in self.effects:
            if effect.is_alive == False: continue
            f = effect.on_appy_effect(effectid=effectid, type=effect.type, *args, **kwargs)
            if f==False: allow_to_apply = False
        
        for func in self.events.get('on_apply_effect') or []:
            f = func(effectid=effectid, type=effect.type, *args, **kwargs)
            if f==False: allow_to_apply = False
        self.game.indent_log -= 1

        if allow_to_apply:
            self.effects.append(effect)

    def on_attacked(self, damage:float, type:str, attacker:Pet, is_true:bool=False, *args, **kwargs):
        
        self.game.indent_log += 1
        for effect in self.effects:
            if effect.is_alive == False: continue
            damage = effect.on_attacked(damage=damage, type=type, attacker=attacker, is_true=is_true, *args, **kwargs) or damage

        for func in self.events.get('on_attacked') or []:
            damage = func(damage=damage, type=type, attacker=attacker, is_true=is_true, *args, **kwargs) or damage
        self.game.indent_log -= 1
        
        self.on_damaged(damage, type, is_true)

    def on_damaged(self, damage:float, type:str=None, is_true:bool=False, *args, **kwargs):
        self.game.indent_log += 1
        for effect in self.effects:
            if effect.is_alive == False: continue
            damage = effect.on_damaged(damage=damage, type=type, is_true=is_true, **kwargs) or damage

        for func in self.events.get('on_damaged') or []:
            damage = func(damage=damage, type=type, is_true=is_true, *args, **kwargs) or damage
        self.game.indent_log -= 1
        
        if not is_true: 
            if type == "physical": damage -= 0.8 * ( (25 + 2 * self.level * self.resistance_physical) / (125 + 2 * self.level * self.resistance_physical) )
            else: damage -= 0.8 * ( (25 + 2 * self.level * self.resistance_magical) / (125 + 2 * self.level * self.resistance_magical) )
        damage = max(0, damage)
        self.health -= damage
        self.health = max(self.health, 0)
    
    def on_healed(self, h: float, *args, **kwargs):
        
        self.game.indent_log += 1
        for effect in self.effects:
            if effect.is_alive == False: continue
            damage = effect.on_healed(health=h, *args, **kwargs) or damage

        for func in self.events.get('on_healed') or []:
            damage = func(health=h, *args, **kwargs) or damage
        self.game.indent_log -= 1

        self.health += h
        self.health = min(self.health, self.max_health)
    
    def on_wp_replenished(self, wp, *args, **kwargs):

        self.game.indent_log += 1
        for effect in self.effects:
            if effect.is_alive == False: continue
            damage = effect.on_wp_replenished(weapoint_point=wp, *args, **kwargs) or damage

        for func in self.events.get('on_damaged') or []:
            damage = func(weapoint_point=wp, *args, **kwargs) or damage
        self.game.indent_log -= 1

        self.weapon_point += wp
        self.weapon_point = min(self.health, self.max_wp)


    # Defaults
    @property
    def status(self):
        return {
            'icon': self.icon,
            'name': self.name,
            'level': self.level,
            'weapon': self.weapon.icon if self.weapon else None,
            'effects': [i.icon for i in self.effects],

            'health': self.health,
            'physical_attack': self.physical_attack,
            'magical_attack': self.magical_attack,
            'resistance_physical': self.resistance_physical,
            'resistance_magical': self.resistance_magical,
            'intelligent': self.intelligent,
            'weapon_point': self.weapon_point,
            'max_health': self.max_health,
            'max_wp': self.max_wp,
        }

    def active(self):
        if self.weapon: self.weapon.active()

        enemies: list[Pet] = self.game.right.pets if self.team=='left' else self.game.left.pets
        enemy_attack = random.choice(enemies)

        self.game.log(f"{self.name} đã tấn công {enemy_attack.name} và gây {self.physical_attack} damage")
        enemy_attack.on_attacked(damage=self.physical_attack, type="physical", attacker=self, is_true=False)
    

class Effect:
    """
    ## Input Pramaters
    - `icon`: icon của effect emoji -> `str`
    - `name`: tên effect -> 'str'
    - `type`: buff/debuff
    - `description`: mô tả kỹ năng -> `str`
    
    - `active`: gọi hiệu ứng khi đến lượt (trước khi sử dụng vũ khí / tấn công)
    - `is_alive`: hiệu ứng còn hoạt động không? đổi thành False nếu muốn tắt
    
    Lưu ý: Các event sẽ được viết như hàm bth, không sử dụng add_event_listener vì khi hết effect sẽ không xóa được event!
    """
    id: str
    icon: str
    name: str
    type: str

    is_alive:bool = True

    def active(self, *args, **kwargs): pass
    def on_turn(self, *args, **kwargs): pass
    def on_appy_effect(self, *args, **kwargs): pass
    def on_attacked(self, *args, **kwargs): pass
    def on_damaged(self, *args, **kwargs): pass
    def on_healed(self, *args, **kwargs): pass
    def on_wp_replenished(self, *args, **kwargs): pass

    def __init__(self, pet) -> None:
        self.pet = pet
        if not hasattr(self, 'name'): self.name = self.id

class Weapon:
    """
    ## Input Pramaters
    - `icon`: icon của weapon emoji -> `str`
    - `name`: tên weapon
    - `information`: kể chuyện -> 'str'
    - `description`: mô tả kỹ năng -> `str`

    - `priority`: mức độ ưu tiên -> `int`
    - `active`: gọi khi sử dụng vũ khí

    ## Built-in Pramaters
    - `game`: class Game
    - `pet`: pet đang cầm vũ khí -> `Pet`
    - `quality`: chất lượng -> `float`
    """
    id: str
    name: str
    icon: str
    information: str
    description: str
    priority: int
    def active(self): pass
    
    game: Game
    pet: Pet
    quality: float

    def __init__(self, weaponmodel) -> None:
        self.id = weaponmodel.weapon_id
        self.quality = weaponmodel.quality
        if not hasattr(self, 'name'): self.name = self.id
    
    def on_game_start(self): pass
    def start_game(self, pet:Pet, game:Game):
        self.game = game
        self.pet = pet
        self.on_game_start()


class Area:
    """
    ## Thông số đầu vào
    - `icon`: biểu tượng của khu vực -> `str`
    - `name`: tên khu vực -> `str`
    - `description`: mô tả khu vực -> `str`
    - `available_pets`: danh sách các pet có sẵn trong khu vực -> `list[str]`
    - `available_weapons`: danh sách các vũ khí có sẵn trong khu vực -> `list[str]`
    """
    icon: str
    name: str
    description: str
    available_pets: list[str]
    available_weapons: list[str]

