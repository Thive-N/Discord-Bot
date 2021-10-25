from discord.ext import commands

from utils.config_parser import ConfigParser

def is_maintainer():
    """
    Simple decorator to check if the author is a maintainer.
    """
    async def predicate(ctx):
        parser = ConfigParser()
        return ctx.author.id in parser.get_maintainers()
    return commands.check(predicate)
