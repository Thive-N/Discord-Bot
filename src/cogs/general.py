from datetime import datetime

import discord

from discord.ext import commands

from utils.standard import StandardEmbed, standard_send

TIME_FORMAT = '%a %d %b %Y'

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def avatar(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author

        description = 'Avatar for: {0}'.format(user.mention)
        embed = StandardEmbed(self.bot, description=description)
        embed.set_image(url=user.avatar_url)

        await standard_send(ctx.channel, embed=embed)


    @commands.command(name='server-info')
    async def server_info(self, ctx):
        guild = ctx.guild
        description = 'Info for: {0}'.format(guild.name)

        time_now = datetime.utcnow()

        created_at = guild.created_at
        created_at_delta = (time_now - created_at).days
        created_at_str = '{0}\n({1} days ago)' \
                .format(created_at.strftime(TIME_FORMAT), created_at_delta)

        categories = len(guild.categories)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)

        channel_str = 'Categories: {0}\nText Channels: {1}\nVoice Channels: {2}' \
                .format(categories, text_channels, voice_channels)

        embed = StandardEmbed(self.bot, description=description)
        embed.add_field(name='Owner', value=guild.owner.mention, inline=True)
        embed.add_field(name='Server ID', value=guild.id, inline=True)
        embed.add_field(name='Members', value=guild.member_count, inline=True)
        embed.add_field(name='Roles', value=len(guild.roles), inline=True)
        embed.add_field(name='Boost Level', value=guild.premium_tier, inline=True)
        embed.add_field(name='Boosts', value=guild.premium_subscription_count, inline=True)
        embed.add_field(name='Created At', value=created_at_str, inline=False)
        embed.add_field(name='Channels', value=channel_str, inline=False)
        embed.set_thumbnail(url=guild.icon_url)

        await standard_send(ctx.channel, embed=embed)


    @commands.command(name='user-info')
    async def user_info(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author

        description = 'Info for: {0}'.format(user.mention)

        time_now = datetime.utcnow()

        nick = user.nick
        if nick is None:
            nick = 'N/A'

        created_at = user.created_at
        created_at_delta = (time_now - created_at).days
        created_at_str = '{0}\n({1} days ago)' \
                .format(created_at.strftime(TIME_FORMAT), created_at_delta)

        joined_at = user.joined_at
        joined_at_delta = (time_now - joined_at).days
        joined_at_str = '{0}\n({1} days ago)' \
                .format(joined_at.strftime(TIME_FORMAT), joined_at_delta)

        boosting_since = user.premium_since

        if boosting_since is None:
            boosting_since_str = 'N/A'

        else:
            boosting_since_delta = (time_now - boosting_since).days
            boosting_since_str = '{0}\n({1} days ago)' \
                    .format(boosting_since.strftime(TIME_FORMAT), boosting_since_delta)

        for i, role in enumerate(user.roles):
            role_mention = role.mention if role.name != '@everyone' else role.name

            if i == 0:
                roles_str = role_mention

            else:
                roles_str += ', {0}'.format(role_mention)

        embed = StandardEmbed(self.bot, description=description)
        embed.add_field(name='Nickname', value=nick, inline=True)
        embed.add_field(name='Name', value=user.name, inline=True)
        embed.add_field(name='User ID', value=user.id, inline=True)
        embed.add_field(name='Created At', value=created_at_str, inline=True)
        embed.add_field(name='Joined At', value=joined_at_str, inline=True)
        embed.add_field(name='Boosting Since', value=boosting_since_str, inline=True)
        embed.add_field(name='Status', value=user.status, inline=False)
        embed.add_field(name='Roles [{0}]'.format(len(user.roles)), value=roles_str, inline=False)
        embed.set_thumbnail(url=user.avatar_url)

        await standard_send(ctx.channel, embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
