from discord.ext import commands

from utils.standard import StandardEmbed, standard_send

class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='test', description='test')
    async def _test(self, ctx):
        embed = StandardEmbed(self.bot, description='Testing cogs')
        await standard_send(ctx.channel, embed=embed)


def setup(bot):
    bot.add_cog(Template(bot))
