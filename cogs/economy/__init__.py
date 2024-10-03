import discord
from models.economy.user import SessionLocal

credit_icon = "💵"
def bt(money:int): return f"{credit_icon} {money:,}"


async def setup(bot: discord.Client) -> None:
    db = SessionLocal()

    from .eco import Eco
    await bot.add_cog(Eco(bot, db))

    from .death import Death
    await bot.add_cog(Death(bot, db))

    from .gamble import Gamble
    await bot.add_cog(Gamble(bot, db))