class Weapon:
    """
    ## Input Pramaters
    - `icon`: icon của pet emoji -> `str`
    - `information`: kể chuyện -> 'str'
    - `description`: mô tả kỹ năng -> `str`

    - `priority`: mức độ ưu tiên -> `int`
    - `active`: gọi khi sử dụng vũ khí

    ## Built-in Pramaters
    - `pet`: pet đang cầm vũ khí -> `Pet`
    - `quality`: chất lượng -> `float`
    """
    id: str
    icon: str
    information: str
    description: str
    active: function
    
    quality: float

    def __init__(self, game, pet, quality: float) -> None:
        self.game = game
        self.pet = pet
        self.quality = quality
