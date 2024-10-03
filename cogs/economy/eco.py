import random
import discord
from discord.ext import commands

from models.economy.user import User, SessionLocal
from sqlalchemy import desc
from datetime import datetime, timedelta

from . import credit_icon, bt

class Eco(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def get_user(self, user_id):
        user = self.db.query(User).filter_by(id=user_id).first()
        if user: return user
        user = User(id=user_id)
        self.db.add(user)
        self.db.commit()
        return user
    
    # Admin
    @commands.command(name="freemoney", help="Give free money (admin only)")
    @commands.is_owner()
    async def freemoney(self, ctx: commands.Context, user_ping: discord.Member, amount: int):
        user = self.get_user(user_ping.id)
        user.credit += amount
        self.db.commit()
        await ctx.send(f"{user_ping.mention} đã nhận được {bt(amount)} free! Hiện {user_ping.mention} đang có {bt(user.credit)}")

    # Basic
    @commands.command(name="cash", aliases=["c", "wallet","credit","money"], help=f"Hiển thị số {credit_icon} của bạn.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def cash(self, ctx):
        user = self.get_user(ctx.author.id)
        await ctx.reply(f"👛 | Bạn hiện có {bt(user.credit)}")
    @commands.command(name="rank", help="Hiển thị bảng rank top 10", aliases=['top'])
    async def rank(self, ctx, amount:int = 10):
        top_users = self.db.query(User).order_by(desc(User.credit)).limit(amount).all()
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
                value=f"{bt(user.credit)}",
                inline=False
            )

        await ctx.send(embed=embed)    
    
    
