import os, json
from app import WhitherBot


if __name__ == '__main__':
    try:
        with open('.secret.json', "r", encoding='utf-8') as f: secret = json.load(f)
    except:
        secret = {
            "SECRET_KEY": "123",
            "DEFAULT_PREFIX": "w",

            "BOT":{
                "ID": "",
                "TOKEN": "",
            },
            
            "WEBSITE": {
                "URL": "localhost",
                "HOST": "0.0.0.0",
                "PORT": 80
            },

            "HAVE_PILLOW": True,
            
            "OWNERS_ID": []
        }

    bot = WhitherBot(secret)
    import threading
    try:
        threading.Thread(target=bot.website.run,
                        kwargs=dict(host=bot.secret['WEBSITE']['HOST'], port=bot.secret['WEBSITE']['PORT']),
                        daemon=True).start()
        threading.Thread(target=bot.run,
                        kwargs=dict(token=secret['BOT']['TOKEN']),
                        daemon=True).start()
    except: pass
    import time
    while True: time.sleep(1)