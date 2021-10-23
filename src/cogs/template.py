from discord.ext import commands

from discord_slash import cog_ext, SlashContext


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test", description="test")
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="Embed Test")
        await ctx.send(embed=embed)


def setup(bot):
    print("loading template")
    bot.add_cog(Template(bot))
