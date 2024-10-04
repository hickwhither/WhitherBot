import discord
from discord import Embed
from discord.ext import commands
import os

async def setup(bot) -> None:
    await bot.add_cog(Developer(bot))

class Developer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """sync the tree"""
        self.bot.tree.clear_commands(guild=None)
        await self.bot.tree.sync()
        # await self.tree.sync(guild = Object(944606508644204546))
        # await self.tree.sync(guild = Object(941346099011133440))
        # await self.tree.sync(guild = Object(1151743010044911656))
        await ctx.reply('Command tree synced.')

    @commands.command(aliases = ['rl','yell'])
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, exts: str = ''):
        """reload cogs"""
        await ctx.typing()
        content = ''
        exts = exts.split(' ')
        no_extension = exts == ['']
        extensions = {}
        self.bot.extra_log = []
        for file in os.listdir('./cogs') if no_extension else exts:
            if (not file.startswith('_') and (os.path.exists(os.path.join('cogs', file)) or file.endswith('.py'))) or not no_extension:
                if file.endswith('.py'): file = file[:-3]
                try:
                    await self.bot.unload_extension(f'cogs.{file}')
                    await self.bot.load_extension(f'cogs.{file}')
                except discord.ext.commands.errors.ExtensionNotLoaded: # Chua load extension
                    extensions[file] = None
                    try:
                        await self.bot.load_extension(f'cogs.{file}')
                    except Exception as e:
                        extensions[file] = e
                except Exception as e: 
                    extensions[file] = e
                else: # Ko loi
                    extensions[file] = None

        for file, error in extensions.items():
                if error:
                    content += f'\❌ `{file}`: **{error}**\n'
                else:
                    content += f'\✅ `{file}`\n'

        content += '\n\n'
        for extra in self.bot.extra_log:
            content += f"From {extra[0]}:\n```{extra[1]}```"

        await ctx.reply(content)
    

    
