from models.economy import get_session

from models.economy.user import UserModel
from models.economy.item import WeaponModel


db = get_session()()

for user in db.query(UserModel).all():
    user: UserModel
    for k, v in user.zoo.items():
        v['caught'] = v['amount']
        v['selled'] = 0
        v['sacrificed'] = 0
        user.zoo[k] = v
    user.zoo.update()

db.commit()

