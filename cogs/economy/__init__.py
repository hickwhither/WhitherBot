import discord

credit_icon = "💵"
def money_beauty(money:int): return f"{credit_icon} {money:,}"


async def setup(bot: discord.Client) -> None:
    from .eco import Eco
    await bot.add_cog(Eco(bot, bot.economy_db))

    from .death import Death
    await bot.add_cog(Death(bot, bot.economy_db))

    from .gamble import Gamble
    await bot.add_cog(Gamble(bot, bot.economy_db))

    from .zoo import Zoo
    await bot.add_cog(Zoo(bot, bot.economy_db))