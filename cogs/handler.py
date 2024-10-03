import discord
from discord import Embed
from discord.ext import commands
import traceback
import os, sys, asyncio
import time
from uuid import uuid4

async def setup(bot) -> None:
    await bot.add_cog(Handler(bot))

class Handler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cooldown_message = {}
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("Không có lệnh :(")
            return

        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.reply("NSFW channel 🔞")
            return
        
        if isinstance(error, commands.NotOwner):
            await ctx.reply("Bạn không phải owner!")
            return

        if isinstance(error, commands.CommandOnCooldown):
            if self.cooldown_message.get(ctx.author.id):
                return
            current_time = time.time()

            msg = await ctx.reply(f"Chờ cho đến khi <t:{int(current_time + error.retry_after)}:R> để sử dụng lệnh.")
            self.cooldown_message[ctx.author.id] = True

            await asyncio.sleep(min(10,error.retry_after))
            await msg.delete()
            if self.cooldown_message.get(ctx.author.id):
                del self.cooldown_message[ctx.author.id]

            return

        # Xử lý lỗi còn lại và lưu chúng vào file log
        error_id = uuid4()
        error_traceback = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

        # Tạo file trong thư mục logs với tên là error_id
        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_filename = f'logs/{error_id}.log'
        with open(log_filename, 'w', encoding='utf-8') as f:
            f.write(f"Error ID: {error_id}\n")
            f.write(f"Command: {ctx.command}\n")
            f.write(f"User: {ctx.author} (ID: {ctx.author.id})\n")
            f.write(f"Guild: {ctx.guild.name if ctx.guild else 'DM'} (ID: {ctx.guild.id if ctx.guild else 'N/A'})\n")
            f.write("\nTraceback:\n")
            f.write(error_traceback)

        # Gửi phản hồi người dùng với mã lỗi
        await ctx.reply(f"An error occurred. Error ID: `{error_id}`. Please report this to the admin.")
    
        # In ra terminal để kiểm tra
        print(f"Ignoring exception in command {ctx.command} (Error ID: {error_id}):", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
