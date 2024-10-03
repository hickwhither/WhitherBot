import os
import discord
from discord import Object, Embed, Message
from discord.ext import commands
import dotenv

class MyBot(commands.Bot):

    def __init__(self):
        from models.prefix import SessionLocal
        self.db = SessionLocal()

        dotenv.load_dotenv()
        self.env = os.environ
        self.default_prefix = "w."

        super().__init__(
            command_prefix = 'w.',
            intents = discord.Intents.all(),
            application_id = self.env['APPLICATION_ID'],
            owner_ids = [
                403476178549211156,
                698339875115630643
            ]
        )
    
    async def get_prefix(self, message: Message):
        if not message.guild: return self.default_prefix # DM
        from models.prefix import Prefix
        result = self.db.query(Prefix).filter_by(guild_id=message.guild.id).first()
        return result.prefix if result else self.default_prefix

    
    async def setup_hook(self):
        for file in os.listdir('cogs'):
            if not file.startswith('_') and (os.path.exists(os.path.join('cogs', file)) or file.endswith('.py')):
                if file.endswith('.py'): file = file[:-3]
                try:
                    await self.load_extension(f'cogs.{file}')
                    print(f'✅ Loaded {file}')
                except Exception as e:
                    print(f'❌ Error {file}: {e}')

    async def on_ready(self):
        print(f'=== Logged as {self.user} ({self.user.id}) ===')
    

if __name__ == '__main__':
    if not os.path.exists('db'):
        os.makedirs('db')
    bot = MyBot()
    bot.run(bot.env['BOT_TOKEN'])