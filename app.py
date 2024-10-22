import os, importlib
import time, random, string
import discord
from discord import Message
from discord.ext.commands import Bot

from flask import *
from flask_login import *

class WhitherWebsite(Flask):
    secret: dict
    bot: 'WhitherBot'
    def __init__(self, secret, bot, name='WhitherFlask'):
        super().__init__(name)
        self.bot = bot
        self.secret = secret
        self.config['SECRET_KEY'] = self.secret['SECRET_KEY']
        
        self.password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(15))
        print(f"Generated password: {self.password}")

        for brp in os.listdir(os.path.dirname('./blueprints/')):
            if brp[0]=='_' or brp[-3:] != '.py': continue
            brp=brp[:-3]
            imported = importlib.import_module(f".{brp}", package='blueprints')
            if hasattr(imported, 'bp'): self.register_blueprint(getattr(imported,'bp'))
        
        import models
        self.db = models.SessionLocal()

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(self)

        @login_manager.user_loader
        def load_user(id):
            return self.db.get(models.UserModel).query.get(id)
        
        

class WhitherBot(Bot):
    secret: dict
    website: 'WhitherWebsite'
    def __init__(self, secret):
        self.secret=secret
        self.website = WhitherWebsite(secret, self)

        self.default_prefix = self.secret['DEFAULT_PREFIX']
        super().__init__(
            command_prefix = self.default_prefix,
            intents = discord.Intents.all(),
            application_id = self.secret['BOT']['ID'],
            owner_ids = self.secret['OWNERS_ID']
        )
    
    
    async def on_message(self, message: Message):
        if message.content.startswith(self.default_prefix):
            message.content = self.default_prefix + message.content[len(self.default_prefix):].strip()
            await self.process_commands(message)
    
    def setup_db(self):
        from models import SessionLocal
        self.economy_db = SessionLocal()

    async def setup_hook(self):
        self.setup_db()
        self.extra_log = []
        for file in os.listdir('cogs'):
            if not file.startswith('_') and (os.path.exists(os.path.join('cogs', file)) or file.endswith('.py')):
                if file.endswith('.py'): file = file[:-3]
                try:
                    await self.load_extension(f'cogs.{file}')
                    print(f'✅ Loaded {file}')
                except Exception as e:
                    print(f'❌ Error {file}: {e}')
        
        print()
        for extra in self.extra_log:
            print(f"From {extra[0]}:\n{extra[1]}")

    async def on_ready(self):
        print(f'=== Logged as {self.user} ({self.user.id}) ===')
        self.start_time = time.time()
    
