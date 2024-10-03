import time, datetime
import discord
from discord import Message
from discord.ext import commands

from models.prefix import SessionLocal, Prefix

async def setup(bot) -> None:
    await bot.add_cog(General(bot))

class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = SessionLocal()  # Tạo session mới
    
    @commands.Cog.listener('on_message')
    async def on_message(self, message: Message):
        prefixes = self.get_prefix(message)
        if isinstance(prefixes, str): prefixes = [prefixes]
        print(message.content)
        for prefix in prefixes:
            if message.content.startswith(prefix):
                message.content = self.bot.default_prefix + message.content[len(prefix):].strip()
                await self.bot.process_commands(message)
                break
    
    def get_prefix(self, message: Message):
        if not message.guild: return self.bot.default_prefix
        from models.prefix import Prefix
        result = self.db.query(Prefix).filter_by(guild_id=message.guild.id).first()
        return [result.prefix, self.bot.default_prefix] if result else self.bot.default_prefix

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def prefix(self, ctx, new_prefix:str =None):
        """Change or get prefix of guild"""
        if ctx.guild is None:
            if new_prefix: await ctx.send(f"Sorry but you cannot change prefix in DM. My default prefix: `{self.bot.default_prefix}`")
            else: await ctx.send(f"My default prefix: `{self.bot.default_prefix}`")
            return
        if new_prefix:
            new_prefix = new_prefix.strip()
            self.db.merge(Prefix(guild_id=ctx.guild.id, prefix=new_prefix))
            self.db.commit()
            await ctx.send(f"Prefix has been changed to: `{new_prefix}`")
        else:
            result = self.db.query(Prefix).filter_by(guild_id=ctx.guild.id).first()
            current_prefix = result.prefix if result else self.bot.default_prefix
            await ctx.send(f"Current prefix: `{current_prefix}`")
    
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
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)
        uptime_str = str(datetime.utcfromtimestamp(uptime_seconds).strftime('%H:%M:%S'))
        await ctx.send(f"Bot đã online trong: {uptime_str}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        """Get my invite link"""
        permissions = discord.Permissions(permissions=8)
        invite_url = discord.utils.oauth_url(self.bot.user.id, permissions=permissions)
        await ctx.send(f"Invite me by this link: {invite_url}")

