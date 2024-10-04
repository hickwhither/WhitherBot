import random
import discord
from discord.ext import commands

from game.pet import Pet
from game.pet import Weapon
from models.economy.user import UserModel
from models.economy.item import WeaponModel
import asyncio

from . import credit_icon, bt

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
def num_subscript(x: int):
    x:str = str(x)
    while len(x)<4: x='0'+x
    return x.translate(SUP)

class Zoo(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        
        from game import GameBase
        self.gamebase = GameBase()
        
        self.pet_hunt = list(self.gamebase.pets.keys())

    def get_user(self, user_id):
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user: return user
        user = UserModel(id=user_id)
        self.db.add(user)
        self.db.commit()
        return user

    @commands.command(name="zoo", help="Nhà tao có nuôi một cục nợ")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def zoo(self, ctx: commands.Context):
        user: UserModel = self.get_user(ctx.author.id)
        pet_ranks: dict[str, list] = {}
        
        for id, param in dict(user.zoo).items():
            pet_class = self.gamebase.pets.get(id)
            pet: Pet = pet_class(param)

            if not param.get('weapon'): weapon = None
            else:
                weapon_class = self.gamebase.weapons.get(param['weapon']['id'])
                weapon: Weapon = weapon_class(param['weapon'])
            
            pet.weapon = weapon
            pet.amount = param['amount']
            
            if not pet_ranks.get(pet.rank): pet_ranks[pet.rank] = []
            pet_ranks[pet.rank].append(pet)

        content = f"🌿 🌱 🌳 {ctx.author.display_name}'s zoo! 🌳 🌿 🌱\n"
        for k in ['Common', 'Uncommon', 'Rare', 'Epic', 'Mythical', 'Gem', 'Legend', 'Fable', 'Bot', 'Hiden', 'Glitch', 'Fallen']:
            if not pet_ranks.get(k): continue
            content += f"{k} **|** {'  '.join(f"{pet.icon}{num_subscript(pet.amount)}" for pet in pet_ranks[k])}\n"
        
        await ctx.reply(content)

    @commands.command(name="hunt", help="Đi săn đến hơi thở cuối cùng")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hunt(self, ctx:commands.Context):
        user: UserModel = self.get_user(ctx.author.id)
        pet_id: str = random.choice(self.pet_hunt)

        
        if user.zoo.get(pet_id): user.zoo[pet_id]['amount'] += 1
        else: user.zoo[pet_id] = {'id': pet_id, 'level': 0, 'amount': 1}
        user.zoo.update()
        self.db.commit()

        pet_class = self.gamebase.pets.get(pet_id)
        pet: Pet = pet_class(user.zoo[pet_id])
        pet.weapon = None
        await ctx.reply(f"Bat duoc trai tim em {pet.icon}")