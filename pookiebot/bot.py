import discord
from discord.ext import commands
import os
import logging
import traceback

from utils.chat_formatter import codebox

COMMAND_PREFIX = "pookie please "

# Set Discord Gatway Intent Flags
# Refer to Gateway Intents Primer in discord.py documentation
# https://discordpy.readthedocs.io/en/latest/intents.html
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    try:
        await bot.load_extension("cogs.basic")
        await bot.load_extension("cogs.currency_conversion")
        await bot.load_extension("cogs.gambling.session")
        await bot.tree.sync()
        print("Finished loading extensions!")
    except Exception as e:
        print(f"Error loading extension: {e}")
    print(f"Logged in as {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    logging.warning(
        f"Command error: {error}\nTraceback: {''.join(traceback.format_tb(error.__traceback__))}"
    )

    embed = discord.Embed(
        title="Command Error",
        description=f"An error occured in command `{ctx.command}`",
        color=discord.Color.red(),
    )

    embed.add_field(name="Error Details", value=codebox(error), inline=False)
    embed.add_field(name="Invoked by", value=ctx.author.mention, inline=True)
    await ctx.send(embed=embed)


def main():
    handler = logging.FileHandler(filename="logs.log", encoding="utf-8", mode="w")

    if (BOT_TOKEN := os.getenv("DISCORD_POOKIE_BOT_TOKEN")) is None:
        raise RuntimeError("Problem accessing bot token!")

    bot.run(BOT_TOKEN, log_handler=handler, root_logger=True)


if __name__ == "__main__":
    main()
