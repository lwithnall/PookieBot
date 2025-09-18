import discord


async def message_user(user: discord.Member, message: str):
    """Helper function to send the player a dm."""
    channel = await user.create_dm()
    await channel.send(message)
