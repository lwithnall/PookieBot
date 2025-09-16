import discord
from discord.ext import commands
import os

COMMAND_PREFIX = "pookie please "


def main():
    if (BOT_TOKEN := os.getenv("DISCORD_POOKIE_BOT_TOKEN")) is None:
        raise RuntimeError("Problem accessing bot token!")

    # Set Discord Gatway Intent Flags
    # Refer to Gateway Intents Primer in discord.py documentation
    # https://discordpy.readthedocs.io/en/latest/intents.html
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


if __name__ == "__main__":
    main()
