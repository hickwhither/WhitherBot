import os, json
from app import WhitherBot

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    BOT_ID = os.environ['BOT_ID']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    OWNERS = list(map(int, os.environ['OWNERS'].split(',')))
    PREFIX = os.environ['PREFIX']
    
    bot = WhitherBot(BOT_ID, OWNERS, PREFIX)

    bot.run(BOT_TOKEN)