from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Game
    from .pet import Pet

class Weapon:
    """
    ## Input Pramaters
    - `icon`: icon của pet emoji -> `str`
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
    icon: str
    information: str
    description: str
    def active(self): pass
    
    game: Game
    pet: Pet
    quality: float

    def __init__(self, game, pet, param:dict) -> None:
        self.game = game
        self.pet = pet
        self.id = param.get('id')
        self.quality = param.get('quality')
