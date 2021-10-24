import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from utils.standard import StandardEmbed, standard_send


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test', description='test')
    async def test(self, ctx):
        """
        generic cog command
        """

        return
        # embed = StandardEmbed(self.bot, description='Testing cogs')
        # await standard_send(ctx.channel, embed=embed)

    @cog_ext.cog_slash(name="test", description="test")
    async def _test(self, ctx: SlashContext):
        """
        slash command template
        """
        return

        # embed = discord.Embed(title="Embed Test")
        # await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Template(bot))
