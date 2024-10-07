import discord
from discord.ext import commands

from game.oop import Pet
from game.oop import Weapon
from models.economy import *
import asyncio

from . import credit_icon, money_beauty

import itertools
import json
import random
import re
import string

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

def randomid():
    return ''.join(random.choices(string.ascii_letters+string.digits, k=6))

class Zoo(commands.Cog):
    def __init__(self, bot: discord.Client, db):
        self.bot = bot
        self.db = db
        
        from game import GameBase
        self.gamebase = GameBase()
        self.bot.extra_log.append(('Zoo', self.gamebase.load_status))
        
        self.all_pet_ids = list(self.gamebase.pets.keys())
        self.all_weapon_ids = list(self.gamebase.weapons.keys())

    def registered_user(self, user_id): return self.db.query(UserModel).get(user_id)

    def get_user(self, user_id):
        user = self.db.query(UserModel).get(user_id)
        if user: return user
        user = UserModel(id=user_id)
        self.db.add(user)
        self.db.commit()
        return user

    def get_weapon(self, id): return self.db.query(WeaponModel).get(id)

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
            row = ''
            for pet in pet_ranks[k]:
                zoo_points += pet.points * pet.caught
                row += f"{pet.icon}{num_subscript(pet.amount)}"
            row = row.strip()
            content += f"{rarity_to_emoji[k]}  {row}\n"
        content += f"**Zoo Points: {zoo_points:,}**"
        
        await ctx.send(content)
    
    @commands.command(name="dex", help="thống số pet")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dex(self, ctx: commands.Context, pet_id: str):
        user: UserModel = self.get_user(ctx.author.id)
        pet_id = self.gamebase.pet_aliases.get(pet_id)
        
        if not pet_id or not user.zoo.get(pet_id):
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
        info += f'**Rank:** {rarity_to_emoji[pet.rank]} {pet.rank}\n'
        info += f'**Điểm:** {pet.points:,}\n'
        info += f'**Bán:** {money_beauty(pet.sell)} | {param.get('selled')} đã bán\n'
        info += f'**Hiến tế:** {pet.sacrifice:,} | {param.get('sacrificed')} đã hiến tế\n'
        embed.add_field(name='',value=info,inline=False)

        blahlbah = f"""
<:Health_Points:1291709800182190183> `{pet.health}` <:Intelligent_point:1291709803248488469> `{pet.intelligent}` <:Weapon_Points:1291709815164502047> `{pet.weapon_point}`
<:Physical_Attack:1291709810374610984> `{pet.physical_attack}` <:Physical_Resistance:1291709812496797696> `{pet.resistance_physical}`
<:Magical_Attack:1291709805710278697> `{pet.magical_attack}` <:Magical_Resistance:1291709808512339998> `{pet.resistance_magical}`
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
            'id': pet_id,

            'level': 0,
            'xp': 0,

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
                       f"🌿 **|** Bạn bat duoc trai tim em:  {pet.icon}")

    
    @commands.command(name="crate", help="Gacha oooo")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def crate(self, ctx: commands.Context):
        user:UserModel = self.get_user(ctx.author.id)
        
        # Kiểm tra nếu người chơi đủ tiền mở hòm
        if user.credit < 100:
            await ctx.reply("Bạn không đủ tiền gacha oooo!")
            return
        
        user.credit -= 100

        weapon_id = random.choice(self.all_weapon_ids)
        weapon_quality = random.uniform(0, 1)
        
        rndid = randomid()
        while self.get_weapon(rndid): rndid = randomid()

        weapondata = WeaponModel(id=rndid, weapon_id=weapon_id, quality=weapon_quality, user_id=user.id)
        self.db.add(weapondata)
        self.db.commit()
        
        weapon_cls = self.gamebase.weapons.get(weapon_id)
        weapon:Weapon = weapon_cls(weapondata)
        
        await ctx.reply(f"Chơi cả lò trái tim em... {weapon.icon} {weapon.name}")


    @commands.group(name="weapon", help='Đồ tự vệ', aliases = ['w'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def weapon(self, ctx: commands.Context):
        user:UserModel = self.get_user(ctx.author.id)
        weapons = user.weapon
        
        if ctx.invoked_subcommand:
            return

        embed = discord.Embed(description=f'''
Các vũ khí vjp pro của {ctx.author.mention}
Thông tin vũ khí: `w weapon info <weaponID>`
Reroll: `w weapon rr <weaponID>` # **In maintain**
Khóa vũ khí: `w weapon lock <weaponID>`
Mở khóa vũ khí: `w weapon unlock <weaponID>`
'''.strip())
        embed.set_author(icon_url=ctx.author.display_avatar.url, name=f"Kho vũ khí của {ctx.author.display_name}")

        weapon_display = ''
        for i in weapons:
            i:WeaponModel
            weapon_cls = self.gamebase.weapons.get(i.weapon_id)
            weapon_model:Weapon = weapon_cls(i)
            
            weapon_display += f"`{i.id}`{weapon_model.icon} {'**' if i.lock else ''}{weapon_model.name}{'**' if i.lock else ''} {int(weapon_model.quality*100)}%\n"
        
        embed.add_field(name='', value=weapon_display.strip())
        embed.set_footer(text='Trang 1/1 (chưa làm trang đâu ớ ớ)')
        
        await ctx.send(embed=embed)
    
    @weapon.command(name="info", help='Đồ tự vệ', aliases = ['w'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def weapon_info(self, ctx: commands.Context, weapon_id:str = None):
        user:UserModel = self.get_user(ctx.author.id)
        weapons = self.db.query(WeaponModel)
        weapon_model:WeaponModel = weapons.get(weapon_id)
        if not weapon_model or weapon_model.user.id != user.id: return await ctx.reply(f'Bạn không sở hữu vũ khí này')
        weapon_cls = self.gamebase.weapons.get(weapon_model.weapon_id)
        weapon: Weapon = weapon_cls(weapon_model)
        embed = discord.Embed(description=f"""
**Name:** {weapon.name}
**Owner:** @{self.bot.get_user(weapon_model.user.id).name}
**ID:** `{weapon_model.id}`
**Quality:** {weapon.quality}
        """.strip())
        embed.set_author(name=weapon.name, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f'Reroll Changes: {weapon_model.reroll_changes} | Reroll Attemps: {weapon_model.reroll_attemps}')

        embed.add_field(name='', value=weapon.information, inline=False)
        embed.add_field(name='', value=weapon.description, inline=False)
        
        await ctx.send(embed=embed)

    @weapon.command(name='lock')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def weapon_lock(self, ctx: commands.Context, weapon_id:str):
        user:UserModel = self.get_user(ctx.author.id)
        weapon:WeaponModel = self.get_weapon(weapon_id)
        if not weapon or weapon.user.id != user.id: return await ctx.reply(f'Bạn không sở hữu vũ khí này')
        weapon.lock = True
        self.db.commit()
        await ctx.reply(f"`{weapon.id}` đã được khóa!")
    
    @weapon.command(name='unlock')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def weapon_unlock(self, ctx: commands.Context, weapon_id:str):
        user:UserModel = self.get_user(ctx.author.id)
        weapon:WeaponModel = self.get_weapon(weapon_id)
        if not weapon or weapon.user.id != user.id: return await ctx.reply(f'Bạn không sở hữu vũ khí này')
        weapon.lock = False
        self.db.commit()
        await ctx.reply(f"`{weapon.id}` đã được mở khóa!")


    @commands.group(name="team", help="Mời anh vào tim em 🤰")
    @commands.cooldown(4, 40, commands.BucketType.user)
    async def team(self, ctx:commands.Context):
        if ctx.invoked_subcommand:
            return
        
        user:UserModel = self.get_user(ctx.author.id)
        team = user.team

        embed = discord.Embed(description="""
`w team rename <pet> <name>` Đổi tên pet
`w team setname <name>` Đổi tên team
`w team setup <pet> <weapon> | <pet> <weapon> ...` (tối đa 4 con) 
 Ví dụ: `w team setup monkey W21dsA | snail | gura`
        """)

        embed.set_author(name=f"{team.get('name') or ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f'Current Streak: {team.get('streak')} | Highest streak: {team.get('max_streak')}')

        cnt = 1
        for pet_param in team.get('pets') or []:
            petpr = user.zoo.get(pet_param['pet'])
            pet_class = self.gamebase.pets.get(petpr['id'])
            pet: Pet = pet_class(petpr)

            if not pet_param.get('weapon'):
                weapon = None
            else:
                
                weapon_model:WeaponModel = self.get_weapon(pet_param['weapon'])
                weapon_class = self.gamebase.weapons.get(weapon_model.weapon_id)
                weapon: Weapon = weapon_class(weapon_model)
            pet.calculate_level()

            embed.add_field(name='', value=f"""
**[{cnt}] {pet.icon} {pet.name}**
Lvl {pet.level} `{petpr['xp']}/inf`
<:Health_Points:1291709800182190183> `{pet.health}` <:Intelligent_point:1291709803248488469> `{pet.intelligent}` <:Weapon_Points:1291709815164502047> `{pet.weapon_point}`
<:Physical_Attack:1291709810374610984> `{pet.physical_attack}` <:Physical_Resistance:1291709812496797696> `{pet.resistance_physical}`
<:Magical_Attack:1291709805710278697> `{pet.magical_attack}` <:Magical_Resistance:1291709808512339998> `{pet.resistance_magical}`
{f'{weapon_model.id} {weapon.icon} {weapon.quality:.2f}' if weapon else ''}
""".strip())
            cnt += 1
        
        await ctx.send(embed=embed)
    
    @team.command(name='rename')
    @commands.cooldown(4, 40, commands.BucketType.user)
    async def team_rename(self, ctx:commands.Context, pet_id:str, *, name:str):
        user:UserModel = self.get_user(ctx.author.id)
        
        pet_id = self.gamebase.pet_aliases[pet_id]
        if not pet_id or not user.zoo.get(pet_id):
            return await ctx.reply("Bạn không sở hữu pet này hoặc không có pet nào như vậy!")

        user.zoo[pet_id]['name'] = name
        user.zoo.update()
        self.db.commit()

        await ctx.reply(f"{pet_id} đã được đổi tên thành {name}")
    
    @team.command(name='setname')
    @commands.cooldown(4, 40, commands.BucketType.user)
    async def team_setname(self, ctx:commands.Context, *, name:str):
        user:UserModel = self.get_user(ctx.author.id)
        user.team['name'] = name
        user.team.update()
        self.db.commit()

        await ctx.reply(f"đã được đổi tên team thành {name}")
    
    @team.command(name='setup')
    @commands.cooldown(4, 40, commands.BucketType.user)
    async def team_setup(self, ctx:commands.Context, *, settxt:str):
        user:UserModel = self.get_user(ctx.author.id)
        
        pet_list = settxt.split('|')
        pets = []


        for i in pet_list:
            content = {}
            spl = i.split()
            if len(spl)==0:
                return await ctx.reply("Lỗi cấu trúc!")
            if len(spl)==1: petid, weaponid = spl[0], None
            else: petid, weaponid = spl[0], spl[1]
            pet_id = self.gamebase.pet_aliases.get(petid)
            
            if not pet_id or not user.zoo.get(pet_id):
                return await ctx.reply(f"Bạn không sở hữu hoặc không có pet {petid}")

            content['pet'] = pet_id
            
            if weaponid:
                weapon_model:WeaponModel = self.get_weapon(weaponid)
                if not weapon_model or weapon_model.user.id != user.id: return await ctx.reply(f'Bạn không sở hữu vũ khí này')
                content['weapon'] = weaponid
            
            pets.append(content)
        
        if len(pets)==0 or len(pets)>4:
            return await ctx.reply(f"Số lượng pet phải nằm trong [1,4]")
        
        # Check for unique pets
        unique_pets = set(pet['pet'] for pet in pets)
        if len(unique_pets) != len(pets):
            return await ctx.reply("Mỗi pet trong team phải là duy nhất!")

        user.team['pets'] = pets
        user.team.update()
        self.db.commit()

        await ctx.reply(f"Sửa đổi team thành công!")


    @commands.command(name='battle', help='Thắng bại tại nạp tiền vào devs', aliases = ['b'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def battle(self, ctx:commands.Context, target: discord.Member):
        if target.bot: return await ctx.reply("Rảnh hả mầy")
        if not self.registered_user(target.id): return await ctx.reply("Thanh niên này hok chơi whitherbot 💦")
        player_data = self.get_user(ctx.author.id)
        target_data = self.get_user(target.id)
        
        player_team = player_data.team.copy()
        target_team = target_data.team.copy()
        
        if not player_team.get('pets'): return await ctx.reply("Hok có team đánh làm qq j 💦")
        if not target_team.get('pets'): return await ctx.reply("Thanh niên này hok có team 💦")

        message = await ctx.send(f"{ctx.author.mention} muốn oán nhau với {target.mention} oooo")

        await message.add_reaction("<:cl:1032661892268826675>")
        await message.add_reaction("⛔")

        def check_reaction_add(reaction:discord.Reaction, user):
                return user == target and reaction.message.id == message.id and str(reaction.emoji) in ["⛔", "<:cl:1032661892268826675>"]
        reaction, user = await self.bot.wait_for('reaction_add', check=check_reaction_add)
        
        if str(reaction.emoji) == "⛔": return await ctx.reply("Thanh niên này sợ vkl 💦")

        for i in range(len(player_team['pets'])):
            player_team['pets'][i]['pet'] = player_data.zoo.get(player_team['pets'][i]['pet'])
            if player_team['pets'][i].get('weapon'): player_team['pets'][i]['weapon'] = self.get_weapon(player_team['pets'][i]['weapon'])
        
        for i in range(len(target_team['pets'])):
            target_team['pets'][i]['pet'] = target_data.zoo.get(target_team['pets'][i]['pet'])
            if target_team['pets'][i].get('weapon'): target_team['pets'][i]['weapon'] = self.get_weapon(target_team['pets'][i]['weapon'])

        player_team['name'] = player_team.get('name') or f"{ctx.author.name}'s team"
        target_team['name'] = target_team.get('name') or f"{target.name}'s team"

        from game import Game
        game = Game(self.gamebase, player_team, target_team)
        game.start_game()

        logs = ''
        
        for i in game.logs:
            for j in i['content']: 
                logs += j+'\n'
        
        game.logs

        embed = discord.Embed()
        embed.set_author(name=f'{ctx.author.name} vs {target.name}', icon_url=ctx.author.display_avatar.url)

        # embed.add_field(name='', value='')
        # embed.add_field(name='', value='')

        message = await ctx.send(embed=embed)
        cnt = 0

        for i in game.logs:
            status = i['status']
            left = status['left']
            right = status['right']

            def create_display(team_status):
                pet_status_list = team_status['pets']
                display = [f'**{team_status['name']}**']
                for pet_status in pet_status_list:
                    single_display = ''
                    single_display += f"L. {pet_status['level']} {pet_status['icon']} {pet_status['name']}\n"
                    single_display += f"""
<:Health_Points:1291709800182190183> `{pet_status['health']}` <:Intelligent_point:1291709803248488469> `{pet_status['intelligent']}` <:Weapon_Points:1291709815164502047> `{pet_status['weapon_point']}`
<:Physical_Attack:1291709810374610984> `{pet_status['physical_attack']}` <:Physical_Resistance:1291709812496797696> `{pet_status['resistance_physical']}`
<:Magical_Attack:1291709805710278697> `{pet_status['magical_attack']}` <:Magical_Resistance:1291709808512339998> `{pet_status['resistance_magical']}`
            """.strip() + '\n'
                    single_display += (pet_status['weapon'] if pet_status['weapon'] else '⬛') + " - "
                    single_display += "".join(i for i in pet_status['effects'])
                    display
                return display

            left_display = create_display(left)
            right_display = create_display(right)
            
            embed.clear_fields()
            for left, right in itertools.zip_longest(left_display, right_display, fillvalue=''):
                embed.add_field(name="", value=left or '')
                embed.add_field(name="", value=right or '')
                embed.add_field(name="\u200b", value="\u200b", inline=False)
            
            embed.description = '\n'.join(j for j in i['content'])


            embed.set_footer(text=f'Turn {cnt}/{len(game.logs)}')

            await message.edit(embed=embed)
            cnt += 1
            await asyncio.sleep(2)

        embed.set_footer(text=f'Ended in {cnt}. {game.winner_content}')
        await message.edit(embed=embed)


    