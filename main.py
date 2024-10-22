import json
from app import WhitherBot


if __name__ == '__main__':
    with open('.secret.json', "r", encoding='utf-8') as f: secret = json.load(f)

    bot = WhitherBot(secret)
    # website = bot.website

    # import threading

    # threading.Thread(target=website.run,
    #                  kwargs=dict(host=secret['WEBSITE']['HOST'], port=secret['WEBSITE']['PORT']),
    #                  daemon=True).start()
    bot.run(secret['BOT']['TOKEN'])