from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .oop import *

import math
import os, sys, importlib


MAXIMUM_TURN = 25


class GameException(Exception): ...
class IdAlreadyExists(GameException):...


increase_gems = {
    'basic': ['💎', 0.05],
    'ring': ['💍', 0.1],
    'ruby': ['♦️', 0.3],
    'sun': ['🔶', 0.5]
}

xp_gems = {
    'letter': ['💌', 0.05],
    'motiv': ['💪', 0.1],
    'heart': ['💓', 0.3],
    'svkmadik': ['🗿', 0.5]
}

"""
pet levels up
from 0 -> 10:      100xp
from 11 -> 20:     500xp
from 21 -> 30:    1000xp
from 31 -> 40:    5000xp
from 41 -> 50:   10000xp
from 50 -> 75:   40000xp
from 75 -> 80:   70000xp
from 80 -> 95:  100000xp
from 95 -> 100: 500000xp
"""


class GameBase:
    """
    Lớp `GameBase` là điểm khởi đầu chính để tải và quản lý các tài nguyên của trò chơi, bao gồm thú cưng, vũ khí, hiệu ứng và khu vực.
    
    Lớp này có các thuộc tính sau:
    - `pets`: Một từ điển ánh xạ tên lớp thú cưng với các lớp thú cưng tương ứng.
    - `pet_aliases`: Một từ điển ánh xạ bí danh thú cưng với tên lớp thú cưng tương ứng.
    - `weapons`: Một từ điển ánh xạ tên lớp vũ khí với các lớp vũ khí tương ứng.
    - `effects`: Một từ điển ánh xạ tên lớp hiệu ứng với các lớp hiệu ứng tương ứng.
    - `areas`: Một từ điển ánh xạ tên khu vực với dữ liệu khu vực tương ứng.
    - `rank_icons`: Một từ điển ánh xạ tên cấp bậc với biểu tượng cấp bậc tương ứng.
    """
    pets: dict
    pet_aliases: dict
    weapons: dict
    effects: dict
    
    areas: dict
    rank_icons: dict

    increase_gems: dict
    xp_gems: dict


    def __init__(self, url_to_cops:str = 'cops'):
        self.pets = {}
        self.pet_aliases = {}
        self.weapons = {}
        self.effects = {}
        
        self.areas = {}
        self.rank_icons = {}

        self.increase_gems = increase_gems
        self.xp_gems = xp_gems
        self.gems = {**self.increase_gems, **self.xp_gems}
        
        self.load_status = ''
        self.load_cops(url_to_cops)

    
    def load_categories(self, rank, url):
        self.current_rank = rank
        for cop in os.listdir(url):
            if os.path.isfile(os.path.join(url, cop)):
                if not cop.startswith('_') and cop.endswith('.py'):
                    cop = cop[:-3]
                    last_url = os.path.join(url, cop)
                    module_name = last_url.replace('/', '.').replace('\\\\', '.').replace('\\', '.')
                    try:
                        if module_name in sys.modules:
                            del sys.modules[module_name]
                        module = importlib.import_module(module_name)

                        if hasattr(module, 'setup'):
                            module.setup(self)
                        else:
                            self.load_status += f'❌ {cop} does not have a setup function\n'
                    except Exception as e:
                        self.load_status += f'❌ Error {cop}: {e}\n'

    def load_area(self, name, url):
        self.current_area = {'pets': [], 'weapons': []}
        for rank in os.listdir(url):
            if os.path.isdir(os.path.join(url, rank)):
                self.load_categories(rank, os.path.join(url, rank))
        
        area_module_name = url.replace('/', '.').replace('\\\\', '.').replace('\\', '.')
        if area_module_name in sys.modules:
            del sys.modules[area_module_name]
        module = importlib.import_module(area_module_name)

        self.current_area.update(dict(
            description=module.description,
            image=module.image))
        self.rank_icons.update(module.icon)

        self.areas[name] = self.current_area

    def load_cops(self, url_to_cops):
        for area in os.listdir(url_to_cops):
            if os.path.isdir(os.path.join(url_to_cops, area)):
                self.load_area(area, os.path.join(url_to_cops, area))
    
    def get_pet_cls(self, id): return self.pets.get(id)
    def get_weapon_cls(self, id): return self.weapons.get(id)

    def add_pet(self, pet: Pet):
        if self.pets.get(pet.__name__): raise IdAlreadyExists(f'Pet `{pet.__name__}` already exists')
        pet.rank = self.current_rank
        self.current_area['pets'].append(pet.__name__)
        self.pets[pet.__name__] = pet
        
        aliases = set()
        aliases.add(pet.__name__)
        if hasattr(pet, 'aliases'): aliases.update(pet.aliases)
        for name in aliases:
            if self.pet_aliases.get(name): raise IdAlreadyExists(f'Aliases `{name}` already exists')
            self.pet_aliases[name] = pet.__name__

    def add_weapon(self, weapon):
        if self.weapons.get(weapon.__name__): raise IdAlreadyExists(f'Weapon {weapon.__name__} already exists')
        self.current_area['weapons'].append(weapon.__name__)
        self.weapons[weapon.__name__] = weapon

    def add_effect(self, effect):
        if self.effects.get(effect.__name__): raise IdAlreadyExists(f'Effect {effect.__name__} already exists')
        self.effects[effect.__name__] = effect

    def add_area(self, area):
        if self.areas.get(area.__name__):
            raise IdAlreadyExists(f'Area {area.__name__} already exists')
        self.areas[area.__name__] = area


class Team:
    game: Game
    gamebase: GameBase
    name: str
    team: str
    
    pets: list[Pet]
    weapons: list[Weapon]

    def __init__(self, game: Game, team, params: dict):
        self.game = game
        self.gamebase = game.gamebase

        self.name = params.get('name') or f'{team} side'
        self.team = team

        self.pets = []
        self.weapons = []

        for param in params['pets']:
            param: dict

            pet_class = self.gamebase.pets.get(param['pet']['id'])
            pet: Pet = pet_class(param['pet'])

            if not param.get('weapon'):
                weapon = None
            else:
                weapon_class = self.gamebase.weapons.get(param['weapon'].weapon_id)
                weapon: Weapon = weapon_class(param['weapon'])
                self.weapons.append(weapon)
            
            pet.start_game(weapon, self.game, team)
            if weapon: weapon.start_game(pet, self.game)
            
            self.pets.append(pet)
    
    @property
    def status(self):
        status = {
            'name': self.name,
            'pets': []
        }
        for pet in self.pets: status['pets'].append(pet.status)
        return status


class Game:
    """
    team{
        name: str
        pet: []
    }
    pet parameter {'id':str, 'name':str, 'level':int, 'weapon':weapon}
    weapon parameter {'id':str, quality: float}
    """
    turn: int = 0
    left: Team
    right: Team
    priority: list[Pet]

    logs: list
    indent_log: int
    status_log: list
    winner: str
    winner_content: str
    

    def __init__(self, gamebase: GameBase, left, right):
        self.gamebase = gamebase

        self.logs = []
        self.indent_log = 0
        self.status_log = []
        self.winner = 'tie'

        self.left = Team(self, 'left', left)
        self.right = Team(self, 'right', right)

        self.priority = self.left.pets + self.right.pets
        def key(pet: Pet):
            if pet.weapon==None: return math.inf
            return pet.weapon.priority
        self.priority.sort(key=key)

        self.indent_log = 0
    
    def log(self, txt):
        self.last_log['content'].append(f"{' '*self.indent_log*2}{txt}")

    def start_game(self):
        self.logs.append({
            'status': self.status,
            'content': ['No logs this turn']
        })
        self.winner_content = None
        
        for i in range(1, MAXIMUM_TURN+1):
            
            self.last_log = {
                'content': [],
                'status': {}
            }

            self.indent_log -= 1
            self.log(f"Lượt #{i}")
            self.indent_log += 1

            self.turn = i
            self.turn_fight()
            self.status_log.append(self.status)
            left_death, right_death = self.check_death()

            self.last_log['status'] = self.status
            self.logs.append(self.last_log)

            if left_death or right_death:
                self.indent_log -= 1
                if left_death and right_death:
                    self.winner_content = 'Không ai còn sống cả!'
                elif right_death:
                    self.winner = 'left'
                    self.winner_content = f'{self.left.name} thắng!'
                elif left_death:
                    self.winner = 'right'
                    self.winner_content = f'{self.right.name} thắng!'
                    
                break
                
        self.indent_log -= 1
        if not self.winner_content: self.winner_content = "Trận đấu quá lâu!"
                

    def turn_fight(self):
        for pet in self.priority:
            pet.on_turn()
    
    @property
    def status(self):
        return {
            'left': self.left.status,
            'right': self.right.status
        }
    
    def check_death(self):
        left_death = True
        right_death = True
        for pet in self.left.pets:
            if pet.health>0: left_death = False
        for pet in self.right.pets:
            if pet.health>0: right_death = False
        return left_death, right_death

