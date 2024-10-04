from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pet import Pet
    from .weapon import Weapon

import os, importlib

class GameException(Exception): ...
class IdAlreadyExists(GameException):...


class GameBase:
    pets: dict = {}
    weapons: dict = {}


    def __init__(self, url_to_cops:str = 'game/cops'):
        self.load_cops(url_to_cops)
    def load_cops(self, url_to_cops):
        for file in os.listdir(url_to_cops):
            if os.path.isdir(os.path.join(url_to_cops, file)):
                    self.load_cops(os.path.join(url_to_cops, file))
                    continue
            if not file.startswith('_') and file.endswith('.py'):
                file = file[:-3]
                module_name = f"{url_to_cops.replace('/', '.').replace('\\\\', '.').replace('\\', '.')}.{file}"
                try:
                    module = importlib.import_module(module_name)

                    if hasattr(module, 'setup'):
                        module.setup(self)
                        print(f'✅ Loaded {file}')
                    else:
                        print(f'❌ {file} does not have a setup function')
                except Exception as e:
                    print(f'❌ Error {file}: {e}')
    
    def get_pet_cls(self, id): return self.pets.get(id)
    def get_weapon_cls(self, id): return self.weapons.get(id)

    def add_pet(self, pet):
        if self.pets.get(pet.__name__): raise IdAlreadyExists
        self.pets[pet.__name__] = pet
    def add_weapon(self, weapon):
        if self.weapons.get(weapon.__name__): raise IdAlreadyExists
        self.weapons[weapon.__name__] = weapon

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

        self.name = params['name'] or f'{team} side'
        self.team = team

        self.pets = []
        self.weapons = []

        for param in params['pets']:
            param: dict

            pet_class = self.gamebase.pets.get(param['id'])
            pet: Pet = pet_class(param)

            if not param.get('weapon'):
                weapon = None
            else:
                weapon_class = self.gamebase.weapons.get(param['weapon']['id'])
                weapon: Weapon = weapon_class(param['weapon'])
                self.weapons.append(weapon)
            
            pet.start_game(weapon, self.game, team)
            if weapon: weapon.start_game(pet, self.game)
            
            self.pets.append(pet)
    


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
    weapons: list[Weapon]

    logs: list
    indent_log: int
    status_log: list
    winner: str
    

    def __init__(self, gamebase: GameBase, left:list[dict], right:list[dict]):
        self.gamebase = gamebase

        self.logs = []
        self.indent_log = 0
        self.status_log = []
        self.winner = 'tie'

        self.left = Team(self, 'left', left)
        self.right = Team(self, 'right', right)

        self.weapons = self.left.weapons + self.right.weapons
        self.weapons.sort(key=lambda x: x.priority)

        self.indent_log = 0
    
    def log(self, txt):
        self.logs.append(f"{' '*self.indent_log*2}{txt}")

    def start_game(self):
        self.status_log.append(self.turn_status())
        for i in range(1, 51):
            
            self.indent_log -= 1
            self.log(f"Lượt #{i}")
            self.indent_log += 1

            self.turn = i
            self.turn_fight()
            self.status_log.append(self.turn_status())
            left_death, right_death = self.check_death()

            self.log("")

            if left_death or right_death:
                self.indent_log -= 1
                if right_death and not left_death:
                    self.winner = 'left'
                    self.log(f"{self.left.name} win!")
                elif left_death and not right_death:
                    self.winner = 'right'
                    self.log(f"{self.right.name} win!")
                else:
                    self.log(f"Hòa! Cả hai đều chết!")
                break
        self.indent_log -= 1
        if self.winner == 'tie': self.log(f"Hòa! Trận đấu kéo dài quá lâu!")
                

    def turn_fight(self):
        for weapon in self.weapons:
            if weapon.pet.health>0: weapon.active()
        
        for i in range(3):
            # print(i, self.left.pets)
            if i < len(self.left.pets):
                if self.left.pets[i].health>0: self.left.pets[i].active()
            if i < len(self.right.pets):
                if self.right.pets[i].health>0: self.right.pets[i].active()
    
    
    def turn_status(self):
        status = {
            'left': [],
            'right': []
        }
        for pet in self.left.pets: status['left'].append(pet.status)
        for pet in self.right.pets: status['right'].append(pet.status)
        
        return status
    
    def check_death(self):
        left_death = True
        right_death = True
        for pet in self.left.pets:
            if pet.health>0: left_death = False
        for pet in self.right.pets:
            if pet.health>0: right_death = False
        return left_death, right_death
