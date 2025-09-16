from discord.ext import commands
from random import choice
from time import perf_counter

from utils.chat_formatter import bold


class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.stopwatches = {}

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
        await ctx.send(choice(["Heads!", "Tails!"]))

    @commands.command()
    async def stopwatch(self, ctx):
        """
        Start or stop stopwatch for relevant user
        Stopwatch is automatically registered to user calling function.
        Users can only have one stopwatch running at a time.
        """
        author = ctx.author
        if author.id not in self.stopwatches:
            self.stopwatches[author.id] = perf_counter()
            await ctx.send(f"Stopwatch started for {author.mention}")
        else:
            stopTime = perf_counter()
            startTime = self.stopwatches.pop(author.id)
            # Time difference returned in seconds to three decimal places
            await ctx.send(f"{stopTime - startTime:.3f} seconds elapsed for {author.mention}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot=bot))
