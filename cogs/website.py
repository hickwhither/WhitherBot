from discord.ext import commands
from flask import *
import threading

async def setup(bot) -> None:
    await bot.add_cog(website(bot))

class website(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
        self.app = Flask(__name__)
        
        @self.app.route('/')
        def home():
            return 'Welcome to the Discord Bot Website!'

        @self.app.route('/status')
        def status():
            return f'Bot is online. Latency: {round(self.bot.latency * 1000)}ms'

    def run_website(self):
        self.app.run(host='0.0.0.0', port=8080)

    @commands.Cog.listener()
    async def on_ready(self):
        threading.Thread(target=self.run_website, daemon=True).start()
        print("Website cog is ready!")

    def run_website(self):
        self.app.run(host='0.0.0.0', port=8080)
