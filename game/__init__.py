from .pet import Pet
from .weapon import Weapon

import os

class GameException(Exception): ...
class IdAlreadyExists(GameException):...

class GameBase:
    pets: dict = {}
    weapons: dict = {}

    def __init__(self, url_to_cops:str = 'game\cops'):
        for file in os.listdir(url_to_cops):
            if not file.startswith('_') and (os.path.exists(os.path.join('cogs', file)) or file.endswith('.py')):
                if file.endswith('.py'): file = file[:-3]
                try:
                    # add ở đây
                    print(f'✅ Loaded {file}')
                except Exception as e:
                    print(f'❌ Error {file}: {e}')
    
    def add_pet(self, pet):
        if self.pets.get(pet.__name__): raise IdAlreadyExists
        self.pets[pet.__name__] = pet
    def add_weapon(self, weapon):
        if self.weapons.get(weapon.__name__): raise IdAlreadyExists
        self.weapons[weapon.__name__] = weapon

class Game:
    left: list[Pet]
    right: list[Pet]
    weapons: list[Weapon]

    def __initialize_pets_(self, pets, team):
        for param in pets:
            pet_class = self.gamebase.pets.get(param['id'])
            pet: Pet = pet_class(self, team, param)

            if team=='left': self.left.append(pet)
            else: self.right.append(pet)
            
            if not param.get('weapon'): pet.weapon = None
            else:
                weapon_class = self.gamebase.weapons.get(param['weapon']['id'])
                pet.weapon = weapon_class(param['weapon'])
                self.weapons.append(pet.weapon)
                

    def __init__(self, gamebase: GameBase, left:list[dict], right:list[dict]):
        self.gamebase = gamebase
        
        self.left = []
        self.right = []
        self.__initialize_pets_(left, 'left')
        self.__initialize_pets_(right, 'right')
        
        self.weapons.sort(lambda x: x.priority)
    
    def start_turn(self):
        ...

    def check_death(self):
        left_death = True
        right_death = True
        for pet in self.left:
            if pet.health>0: left_death = False
        for pet in self.right:
            if pet.health>0: right_death = False
        return left_death, right_death
    
    def turn_status(self):
        status = {
            'left': [],
            'right': []
        }
        for pet in self.left:
            pet.status
