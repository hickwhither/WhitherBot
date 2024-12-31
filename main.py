import os, json
from app import WhitherBot

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    BOT_ID = os.environ['BOT_ID']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    PREFIX = os.environ['PREFIX']
    
    bot = WhitherBot(BOT_ID, PREFIX)

    bot.run(BOT_TOKEN)