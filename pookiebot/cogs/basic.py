from discord.ext import commands
from random import choice

from utils.chat_formatter import bold


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, text: str):
        """Send user provided text."""
        await ctx.send(text)

    @commands.command(usage="<first> <second> [others...]")
    async def choice(self, ctx, *choices):
        """
        Choose single option from choices provided by user.
        User must provided at least two options to pick from.

        Options are space-seperated.
        Options including white-space should be enclosed in double quotes.
        """
        if len(choices) < 2:
            await ctx.send("Not enough options provided.")
        else:
            await ctx.send(choice(choices))

    @commands.command()
    async def coin(self, ctx):
        """Flip a (virtual) coin."""
        await ctx.send(bold(choice(["Heads!", "Tails!"])))


async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot=bot))
