from discord.ext import commands
from discord_slash import SlashCommand, SlashContext


def getToken():
    import os
    if not(os.path.exists("token")):
        print("token does not exsist\ncreate a file called token with a discord token inside it")
        return None
    with open("token", "r") as f:
        return f.read()


if __name__ == "__main__":
    token = getToken()

    bot = commands.Bot(command_prefix='!')
    slash = SlashCommand(bot)
    bot.load_extension("cogs.template")
    bot.run(token)
