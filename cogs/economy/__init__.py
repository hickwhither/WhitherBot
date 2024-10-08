import discord

credit_icon = "💵"
def money_beauty(money:int): return f"{credit_icon} {money:,}"


async def setup(bot: discord.Client) -> None:
    from .eco import Eco
    await bot.add_cog(Eco(bot))

    from .death import Death
    await bot.add_cog(Death(bot))

    from .gamble import Gamble
    await bot.add_cog(Gamble(bot))

    from .zoo import Zoo
    await bot.add_cog(Zoo(bot))