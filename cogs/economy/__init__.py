import discord
from models.economy import get_session

credit_icon = "💵"
def bt(money:int): return f"{credit_icon} {money:,}"


async def setup(bot: discord.Client) -> None:
    db = get_session()()

    from .eco import Eco
    await bot.add_cog(Eco(bot, db))

    from .death import Death
    await bot.add_cog(Death(bot, db))

    from .gamble import Gamble
    await bot.add_cog(Gamble(bot, db))

    from .zoo import Zoo
    await bot.add_cog(Zoo(bot, db))