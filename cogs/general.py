from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import WhitherBot

import time, datetime
import discord
from discord import Message
from discord.ext import commands

async def setup(bot) -> None:
    await bot.add_cog(General(bot))

class General(commands.Cog):
    bot: WhitherBot
    def __init__(self, bot: WhitherBot) -> None:
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        """Test my respond time"""
        latency = round(self.bot.latency * 1000)  # Độ trễ tính bằng ms
        await ctx.send(f"Pong! Độ trễ: {latency}ms")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def uptime(self, ctx):
        """How long I've been up"""
        await ctx.send(f"Bot đã online: <t:{int(self.bot.start_time)}:R>")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        """Get my invite link"""
        permissions = discord.Permissions(permissions=8)
        invite_url = discord.utils.oauth_url(self.bot.user.id, permissions=permissions)
        button = discord.ui.Button(label="Invite me", url=invite_url)
        view = discord.ui.View()
        view.add_item(button)
        await ctx.send("Click the button below to invite me:", view=view)

