import random
from .weapon import Weapon

class Pet:
    """
    ## Input Pramaters
    - `icon`: icon của pet emoji -> `str`
    - `information`: kể chuyện -> 'str'
    - `description`: mô tả kỹ năng -> `str`
    
    - Thông số cơ bản: `health`, `strength`, `resistance`, `intelligent`, `weapon_point` -> `int`
    - `sell`: nhận được khi sell
    - `sacrifice`: nhận được khi sacrifice

    - `active`: gọi khi đến lượt (đánh thường)
    - `calculate_level`: tính lại các thông số dựa theo level

    ## Built-in Pramaters
    - `name`: tên -> `str`
    - 'level': cấp độ -> `int`
    - `weapon`: vũ khí -> `Weapon`
    - `team`: "left"/"right" -> `str`
    - `health`, `strength`, `resistance`, `intelligent`, `weapon_point` sẽ được tính lại bằng super().__init__() dựa trên level


    ## Events
    - `on_attacked`: bị tấn công
    - `on_heal`: được hồi máu
    - `on_wp_replenish`: được hồi WP

    ## Add event listener(name, func)
    - `on_attack`: truyền vào (damage, attacker, is_true) và trả về damage nếu có đổi giá trị
    - `on_heal`: truyền vào (health) và trả về health nếu có đổi giá trí
    - `on_wp_replenish`: truyền vào (wp) và trả về wp nếu có đổi giá trí
    """
    icon: str
    information: str
    description: str

    sell: int
    sacrifice: int

    health: int # HP
    strength: int # STR
    resistance: int # RES
    intelligent: int # INT
    weapon_point: int # WP

    active: function

    max_health: int
    max_wp: int

    name: str
    weapon: Weapon
    team: str # left/right

    events: dict[list[function]] = {}

    def __init__(self, game, team:str, param:dict):
        self.game = game
        self.team = team # left/right
        self.param = param
        
        # Input pramaters set
        self.name = param['name'] or self.__name__
        self.level = param['level']
        
        self.calculate_level()
    


    # Default
    def calculate_level(self):
        self.health = self.health * self.level * 2 + 500
        self.strength = self.strength * self.level + 100
        self.resistance = self.resistance * self.level * 2 + 100
        self.intelligent = self.intelligent * self.level * 2 + 300
        self.weapon_point = self.weapon_point * self.level * 2 + 500
        self.max_health = self.health
        self.max_wp = self.weapon_point
    
    def active(self):
        # teammates:list[Pet] = self.game.left if self.team=='left' else self.game.right
        enemies:list[Pet] = self.game.right if self.team=='left' else self.game.left
        if self.pet.weapon_point < self.cost: return
        random.choice(enemies).on_attacked(self.pet.strength*self.str_damage, self, False)
        random.choice(enemies).on_attacked(self.pet.intelligent*self.int_damage, self, False)
    
    
    @property
    def status(self):
        return {
            'name': self.name,
            'level': self.level,
            'weapon': self.weapon.id,
            'pramaters':{
                'health': self.health,
                'strength': self.strength,
                'resistance': self.resistance,
                'intelligent': self.intelligent,
                'weapon_point': self.weapon_point,
                'max_health': self.max_health,
                'max_wp': self.max_wp,
            }
        }



    # Pet
    def add_event_listener(self, name:str, func:function, *args, **kwargs):
        if not self.events.get(name): self.events[name] = []
        self.events[name].append(func, *args, **kwargs)
    
    def on_attacked(self, damage: float, attacker: 'Pet', is_true: bool = False):
        total_damage = damage

        for func in self.events.get('on_attacked') or []:
            damage = func(damage, attacker, is_true)
        
        self.health -= total_damage
        total_damage -= self.strength
        total_damage = max(0, total_damage)

        self.health -= total_damage
        self.health = max(self.health, 0)
        
        return total_damage
        
    def on_heal(self, h: float):
        self.health += h
        self.health = min(self.health, self.max_health)
    
    def on_wp_replenish(self, wp):
        self.weapon_point += wp
        self.weapon_point = min(self.health, self.max_wp)



