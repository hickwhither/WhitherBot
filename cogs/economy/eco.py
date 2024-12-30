import random
import discord
from discord.ext import commands

from models import UserModel
from sqlalchemy import desc
from datetime import datetime, timedelta

from . import credit_icon, money_beauty

class Eco(commands.Cog):
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
    
    # Admin
    @commands.command(name="freemoney", help="Give free money (admin only)")
    @commands.is_owner()
    async def freemoney(self, ctx: commands.Context, a: discord.Member|int, b:discord.Member|int):
        if isinstance(b, int) and isinstance(a, discord.Member): user_ping, amount = a, b
        elif isinstance(a, int) and isinstance(b, discord.Member): user_ping, amount = b, a
        else:
            raise commands.BadArgument('Phải là một người với một số!')
        user = self.get_user(user_ping.id)
        user.credit += amount
        self.db.commit()
        await ctx.send(f"{user_ping.mention} đã nhận được {money_beauty(amount)} free! Hiện {user_ping.mention} đang có {money_beauty(user.credit)}")

    @commands.command(name="give", help="Chuyển tiền cho người khác")
    @commands.is_owner()
    async def give(self, ctx: commands.Context, a: discord.Member | int, b: discord.Member | int):
        if isinstance(b, int) and isinstance(a, discord.Member):
            recipient, amount = a, b
        elif isinstance(a, int) and isinstance(b, discord.Member):
            recipient, amount = b, a
        else:
            raise commands.BadArgument('Phải là một người với một số!')
        
        if amount <= 0:
            await ctx.send("Số tiền phải lớn hơn 0!")
            return

        sender = self.get_user(ctx.author.id)
        if sender.credit < amount:
            await ctx.send(f"Bạn không đủ tiền! Bạn chỉ có {money_beauty(sender.credit)}.")
            return

        receiver = self.get_user(recipient.id)
        sender.credit -= amount
        receiver.credit += amount
        self.db.commit()

        await ctx.send(f"{ctx.author.mention} đã chuyển {money_beauty(amount)} cho {recipient.mention}!\n"
f"Số dư hiện tại của {ctx.author.mention}: {money_beauty(sender.credit)}\n"
f"Số dư hiện tại của {recipient.mention}: {money_beauty(receiver.credit)}")


    # Basic
    @commands.command(name="cash", aliases=["c", "wallet","credit","money"], help=f"Hiển thị số {credit_icon} của bạn.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def cash(self, ctx):
        user = self.get_user(ctx.author.id)
        await ctx.reply(f"👛 | Bạn hiện có {money_beauty(user.credit)}")
    @commands.command(name="rank", help="Hiển thị bảng rank top 10", aliases=['top'])
    async def rank(self, ctx, amount:int = 10):
        top_users = self.db.query(UserModel).order_by(desc(UserModel.credit)).limit(amount).all()
        amount = min(amount, len(top_users))

        if not top_users:
            await ctx.reply("Không có ai trong bảng xếp hạng!")
            return

        embed = discord.Embed(
            title="Bảng xếp hạng tiền",
            description=f"Top {amount} rich",
            color=discord.Color.gold()
        )

        for index, user in enumerate(top_users, start=1):
            member = ctx.guild.get_member(user.id)  # Lấy thông tin người dùng từ ID
            username = member.display_name if member else f"User ID: {user.id}"
            embed.add_field(
                name=f"{index}. {username}",
                value=f"{money_beauty(user.credit)}",
                inline=False
            )

        await ctx.send(embed=embed)    
    
    
    @commands.command(name="daily", help="Nhận tiền hàng ngày")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        user = self.get_user(ctx.author.id)
        user.credit += 500
        self.db.commit()
        await ctx.reply(f"🎉 | Bạn đã nhận được {money_beauty(500)} hàng ngày! Bạn hiện có {money_beauty(user.credit)}"
                        f"\nNhớ quay lại sau 24h nữa nhé!")
        