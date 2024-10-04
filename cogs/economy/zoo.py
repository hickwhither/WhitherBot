import discord
from discord.ext import commands

from game.pet import Pet
from game.pet import Weapon
from models.economy.user import UserModel
from models.economy.item import WeaponModel
import asyncio

from . import credit_icon, money_beauty

import json
import random
import re

rarity_to_emoji = {
    'Common':'<:common:1291671340037836841>',
    'Uncommon':'<:uncommon:1291671369490366464>',
    'Rare':'<:rare:1291671367338692609>',
    'Epic':'<:epic:1291671341984120883>',
    'Mythical':'<:mythical:1291671365199335486>',
    'Gem':'<a:gem:1291671352146788354>',
    'Legend':'<a:legend:1291671363089596517>',
    'Fable':'<a:fable:1291671349160575047>',
    'Bot':'<a:bot:1291671338079227914>',
    'Hidden':'<a:hidden:1291671361043042304>',
    'Glitch':'<a:glitch:1291671357720891402>',
    'Fallen':':grey_heart:',
}
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
        self.bot.extra_log.append(('Zoo', self.gamebase.load_status))
        
        self.all_pet_ids = list(self.gamebase.pets.keys())
        self.all_weapon_ids = list(self.gamebase.weapons.keys())

    def get_user(self, user_id):
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user: return user
        user = UserModel(id=user_id)
        self.db.add(user)
        self.db.commit()
        return user

    @commands.command(name="zoo", help="Nhà tao có nuôi một cục nợ", aliases=['z'])
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
            pet.caught = param['caught']
            
            if not pet_ranks.get(pet.rank): pet_ranks[pet.rank] = []
            pet_ranks[pet.rank].append(pet)

        content = f"🌿 🌱 🌳 **{ctx.author.display_name}'s zoo!** 🌳 🌿 🌱\n"
        
        zoo_points = 0
        for k in ['Common', 'Uncommon', 'Rare', 'Epic', 'Mythical', 'Gem', 'Legend', 'Fable', 'Bot', 'Hidden', 'Glitch', 'Fallen']:
            if not pet_ranks.get(k): continue
            content += f"{rarity_to_emoji[k]}  {'  '.join(f"{pet.icon}{num_subscript(pet.amount)}" for pet in pet_ranks[k])}\n"
            zoo_points += pet.points * pet.caught
        content += f"**Zoo Points: {zoo_points:,}**"
        
        await ctx.send(content)
    
    @commands.command(name="dex", help="thống số pet")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dex(self, ctx: commands.Context, pet_id: str):
        user: UserModel = self.get_user(ctx.author.id)
        pet_id = self.gamebase.pet_aliases[pet_id]
        
        if not user.zoo.get(pet_id):
            return await ctx.reply("Bạn không sở hữu pet này hoặc không có pet nào như vậy!")
        
        param = user.zoo.get(pet_id)
        pet_class = self.gamebase.pets.get(pet_id)
        pet: Pet = pet_class(param)

        if not param.get('weapon'): weapon = None
        else:
            weapon_class = self.gamebase.weapons.get(param['weapon']['id'])
            weapon: Weapon = weapon_class(param['weapon'])
        
        pet.weapon = weapon
        
        embed = discord.Embed(title=f"{pet.icon} {pet.id}", description=f"*{pet.description}*")

        info = ""
        info += f'**Nickname:** {pet.name}\n'
        info += f'**Count:** {param['amount']}\n'
        info += f'**Rank:** {pet.rank}\n'
        info += f'**Điểm:** ...\n'
        info += f'**Bán:** {money_beauty(pet.sell)} | {param.get('selled')} đã bán\n'
        info += f'**Hiến tế:** {pet.sacrifice} | {param.get('sacrificed')} đã hiến tế\n'
        embed.add_field(name='',value=info,inline=False)

        blahlbah = f"""
<:Health_Points:1291709800182190183> `{pet.health}` <:Intelligent_point:1291709803248488469> `{pet.intelligent}` <:Weapon_Points:1291709815164502047> `{pet.weapon_point}`
<:Physical_Attack:1291709810374610984> `{pet.physical_attack}` <:Physical_Resistance:1291709812496797696> `{pet.resistance_magical}`
<:Magical_Attack:1291709805710278697> `{pet.magical_attack}` <:Magical_Resistance:1291709808512339998> `{pet.resistance_physical}`
""".strip()
        embed.add_field(name='',value=f'{blahlbah}',inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="hunt", help="Đi săn đến hơi thở cuối cùng", aliases=['h'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hunt(self, ctx:commands.Context):
        user: UserModel = self.get_user(ctx.author.id)
        pet_id: str = random.choice(self.all_pet_ids)

        
        if user.zoo.get(pet_id):
            user.zoo[pet_id]['amount'] += 1
            user.zoo[pet_id]['caught'] += 1
        else: user.zoo[pet_id] = {
            'id': pet_id, 'level': 0,
            'amount': 1,
            'caught': 1,
            'selled': 0,
            'sacrificed': 0,
        }
        user.zoo.update()
        self.db.commit()

        pet_class = self.gamebase.pets.get(pet_id)
        pet: Pet = pet_class(user.zoo[pet_id])
        
        if not user.zoo.get(pet_id).get('weapon'): weapon = None
        else:
            weapon_class = self.gamebase.weapons.get(user.zoo.get(pet_id)['weapon']['id'])
            weapon: Weapon = weapon_class(user.zoo.get(pet_id)['weapon'])
        
        pet.weapon = weapon
        pet.amount = user.zoo.get(pet_id)['amount']
        await ctx.send(f"🌱 **|** {ctx.author.display_name} đã dùng các gem: Có nịt" + '\n' +
                       f"🌿   **|** Bạn bat duoc trai tim em:  {pet.icon}")

    @commands.command(name="crate", help="Gacha oooo")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def crate(self, ctx: commands.Context):
        # Lấy user từ database
        user:UserModel = self.get_user(ctx.author.id)
        
        # Kiểm tra nếu người chơi đủ tiền mở hòm
        if user.credit < 100:
            await ctx.reply("You don't have enough credits to open a crate!")
            return

        # Trừ 100 credit khi mở hòm
        user.credit -= 100
        self.db.commit()

        # Gacha để chọn ngẫu nhiên vũ khí
        weapon_id = random.choice(self.all_weapon_ids)
        weapon_quality = random.uniform(0, 1)  # Chọn chất lượng vũ khí là một số float từ 0 đến 1

        # Thêm vũ khí vào kho của người chơi
        user.inventory.append({'type': 'Weapon', 'id': weapon_id, 'quality': weapon_quality})

        # Thông báo kết quả mở hòm
        await ctx.reply(f"Vì chưa gảnh làm nên xem đỡ: `{weapon_id}` with quality: `{weapon_quality:.2f}`.")

    @commands.command(name="weapon", help="Gacha oooo", aliases=['w'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def weapon(self, ctx: commands.Context):
        user:UserModel = self.get_user(ctx.author.id)
        weapons = list(filter(lambda x: x['type']=='Weapon', user.inventory))

        await ctx.reply(f"Vì chưa gảnh làm nên xem đỡ: ```{json.dumps(weapons, indent=4)}```.")
