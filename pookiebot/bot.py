import discord
from discord.ext import commands
import os
import logging

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
        await bot.tree.sync()
    except Exception as e:
        print(f"Error loading extension: {e}")
    print(f"Logged in as {bot.user}")


def main():
    handler = logging.FileHandler(
        filename="logs.log", encoding="utf-8", mode="w")

    if (BOT_TOKEN := os.getenv("DISCORD_POOKIE_BOT_TOKEN")) is None:
        raise RuntimeError("Problem accessing bot token!")

    bot.run(BOT_TOKEN, log_handler=handler, root_logger=True)


if __name__ == "__main__":
    main()
