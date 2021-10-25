import discord

from discord.ext import commands

from utils.standard import StandardEmbed, standard_send

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def mball(self, ctx, *, question: str=None):
        if question is None:
            response = 'There is no question to answer'

        else:
            import random

            responses = (
                'It is certain',
                'Without a doubt',
                'You may rely on it',
                'Yes, definitely',
                'It is decidedly so',
                'As I see it, yes',
                'Most likely',
                'Yes',
                'Outlook good',
                'Signs point to yes',

                'Reply hazy, try again',
                'Better not tell you now',
                'Ask again later',
                'Cannot predict now',
                'Concentrate and ask again',

                'Don\'t count on it',
                'Outlook not so good',
                'My sources say no',
                'Very doubtful',
                'My reply is no',
            )

            response = random.choice(responses)

        await standard_send(ctx.channel, content=response)


    @commands.command()
    async def rps(self, ctx, user_choice):

        # this method was stupid, but fun

        import random

        options = ('rock', 'paper', 'scissors')

        user_choice = user_choice.lower()

        if user_choice not in options:
            content='Invalid option: {0}'.format(user_choice)
            await standard_send(ctx.channel, content=content)
            return

        bot_choice = random.choice(options)

        if user_choice == bot_choice:
            winner = 'Draw'

        else:
            user_choice_index = options.index(user_choice)
            bot_choice_index = options.index(bot_choice)

            if user_choice_index > bot_choice_index:
                bigger = ctx.author
                smaller = self.bot.user

            else:
                bigger = self.bot.user
                smaller = ctx.author

            winner = bigger.mention if (user_choice_index + bot_choice_index) & 1 \
                    else smaller.mention

        embed = StandardEmbed(self.bot, description='Rock, Paper, Scissors')
        embed.add_field(name='{0} Chose'.format(self.bot.user.name), value='`{0}`'.format(bot_choice.capitalize()))
        embed.add_field(name='{0} Chose'.format(ctx.author.display_name),
                value='`{0}`'.format(user_choice.capitalize()))
        embed.add_field(name='Winner', value=winner, inline=False)

        await standard_send(ctx.channel, embed=embed)


    @commands.command()
    async def roll(self, ctx):
        from random import randint

        content = '{0} rolled {1}!'.format(user.display_name,
                randint(1, 6))

        await standard_send(ctx.channel, content=content)


def setup(bot):
    bot.add_cog(Fun(bot))
