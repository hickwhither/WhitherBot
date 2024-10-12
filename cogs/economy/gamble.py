import random
import discord
from discord.ext import commands

from models.economy import UserModel
import asyncio

from . import credit_icon, money_beauty

class Gamble(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def get_user(self, user_id):
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user: return user
        user = UserModel(id=user_id)
        self.db.add(user)
        self.db.commit()
        return user

    @commands.command(name="coinflip", help="Chơi trò chơi tung đồng xu với cược và mặt xu.", aliases=['cf'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, ctx: commands.Context, amount: int|str=1, choice: str = "heads"):
        if choice == 't': choice = 'tails'
        if choice == 'h': choice = 'heads'
        user = self.get_user(ctx.author.id)
        if amount == "all":
            amount = user.credit
        if not isinstance(amount, int):
            await ctx.send(f"{credit_icon} phải là một số nguyên.")
            return
        amount = min(amount, 1000000)
        if amount > user.credit:
            await ctx.send(f"Bạn không có đủ {credit_icon} để đặt cược.")
            return
        if amount <= 0:
            await ctx.send(f"Số {credit_icon} phải là dương.")
            return
        
        user.credit -= amount
        self.db.commit()

        if choice not in ["heads", "tails"]:
            await ctx.send("Chọn một trong hai mặt xu: heads hoặc tails.")
            return

        result = random.choices([True, False], weights=[0.6, 0.4])[0]

        message: discord.Message = await ctx.send(f"{ctx.author.display_name} đã cược {money_beauty(amount)} và chọn mặt {choice}\nĐồng xu đang bay... ⁉️")
        await asyncio.sleep(2)

        if result:
            user.credit += 2*amount
            await message.edit( content=
f"""{ctx.author.display_name} đã cược {money_beauty(amount)} và chọn mặt {choice}
Đồng xu đang bay... {choice} và thắng được {money_beauty(amount*2)}!"""
                )
        else:
            await message.edit( content=
f"""{ctx.author.display_name} đã cược {money_beauty(amount)} và chọn mặt {choice}
Đồng xu đang bay... {"heads" if choice=="tails" else "heads"} và mất tất =))"""
                )
        self.db.commit()

    
    @commands.command(name="slots", help="Chơi trò quay slots.", aliases=['s'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slots(self, ctx: commands.Context, amount: int|str=1):
        user = self.get_user(ctx.author.id)
        if amount == "all":
            amount = user.credit
        if not isinstance(amount, int):
            await ctx.send(f"{credit_icon} phải là một số nguyên.")
            return
        amount = min(amount, 1000000)
        if amount > user.credit:
            await ctx.send(f"Bạn không có đủ {credit_icon} để đặt cược.")
            return
        if amount <= 0:
            await ctx.send(f"Số {credit_icon} phải là dương.")
            return
        
        user.credit -= amount
        self.db.commit()

        message = await ctx.send(
f"""` ___SLOTS___ `
`             ` {ctx.author.display_name} đã cược {money_beauty(amount)}
`\\___________/`"""
            )
        
        async def editt(message: discord.Message, result, extra=""):
            await message.edit(
                content=
f"""` ___SLOTS___ `
` `{' | '.join(i for i in result)}` ` {ctx.author.display_name} đã cược {money_beauty(amount)} {extra}
`\\___________/`"""
                )
        
        emojis = [':cucumber:', ':heart:', ':cherries:', ':dollar:', ':fire:']
        weights = [0.4, 0.25, 0.2, 0.1, 0.05]

        pos = {
            ':cucumber:': 0,
            ':heart:': 1,
            ':cherries:': 2,
            ':dollar:': 3,
            ':fire:': 4
        }

        multiplier = {
            ':cucumber:': 1,
            ':heart:': 2,
            ':cherries:': 3,
            ':dollar:': 4,
            ':fire:': 10
        }
        result = ['<:huanrose:942677994680516629>' for _ in range(3)]
        await editt(message, result)

        await asyncio.sleep(1)

        result[0] = random.choices(emojis, weights=weights)[0]
        weights[pos[result[0]]] += 0.4
        await editt(message, result)
        await asyncio.sleep(1)
        
        result[2] = random.choices(emojis, weights=weights)[0]
        weights[pos[result[2]]] += 0.4
        await editt(message, result)
        await asyncio.sleep(1)

        result[1] = random.choices(emojis, weights=weights)[0]
        weights[pos[result[1]]] += 0.4
        await editt(message, result)
        await asyncio.sleep(2)

        if result[0] == result[1] == result[2]:
            emoji = result[0]
            reward = amount * multiplier[emoji]
            user.credit += reward
            self.db.commit()
            await editt(message, result, extra=f'đã quay trúng {emoji}, idol nhận được {money_beauty(reward)}!')
        else:
            await editt(message, result, extra=f"và đã thua tất =))")

