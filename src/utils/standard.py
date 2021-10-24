import discord

class StandardEmbed(discord.Embed):
    def __init__(self, bot, **kwargs):
        """
        Construct an instance of StandardEmbed.

        :param Bot bot: An instance of Bot
        """
        from datetime import datetime

        kwargs['timestamp'] = datetime.utcnow()

        if kwargs.get('colour') is kwargs.get('colour') is None:
            kwargs['colour'] = 0xaaffaa

        super().__init__(**kwargs)

        self.set_footer(text=bot.user, icon_url=bot.user.avatar_url)


async def standard_send(channel, **kwargs):
    """
    Safely send a message to a channel.

    :param discord.TextChannel: The channel to send a message to
    """
    # default is to prevent all mentions
    if kwargs.get('allowed_mentions') is None:
        kwargs['allowed_mentions'] = discord.AllowedMentions.none()

    await channel.send(**kwargs)
