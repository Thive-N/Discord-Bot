#!/usr/bin/env python3

from discord_slash import SlashCommand
import discord

from discord.ext import commands

from utils.config_parser import ConfigParser
from utils.decorators import is_maintainer
from utils.extension_manager import ExtensionManager
from utils.standard import standard_send

class Bot(commands.Bot):
    # default extensions
    _extensions = (
        'general',
        'fun',
    )

    def __init__(self):
        """
        Create an instance of Bot after setting intents, command_prefix
        and loading the default cogs.
        """
        super().__init__(intents=discord.Intents.all(),
                         command_prefix=self.get_prefix)

        parser = ConfigParser()
        self.default_prefix = parser.get_prefix()

        ExtensionManager.manage(self, self._extensions)


    async def get_prefix(self, message) -> str:
        """
        This function can be modified later on for custom prefixes
        on a per server basis.

        :param discord.Message message: A message sent by a user
        :return: The custom prefix (at some point possibly)
        :rtype: str
        """
        return self.default_prefix


    def get_token(self):
        """
        Check if the token file exists and if it does, return the
        contents after stripping leading and trailing whitespace.

        :return: The token
        :rtype: str
        """
        import os

        if not os.path.exists('./src/token'):
            print(
                'token does not exist\ncreate a file called token with a discord token inside it')

        else:
            with open('./src/token') as f:
                return f.read().strip()


    def run(self):
        """
        Run the bot if and only if the token file exists.
        """
        token = self.get_token()

        if token is not None:
            super().run(token.strip())


if __name__ == '__main__':
    bot = Bot()

    @bot.command(name='load-extensions')
    @is_maintainer()
    async def load_extensions(ctx, *, extensions: str):
        embed = ExtensionManager.manage(bot, extensions.split(),
                action=ExtensionManager.LOAD, return_as_embed=True)

        await standard_send(ctx.channel, embed=embed)


    @bot.command(name='unload-extensions')
    @is_maintainer()
    async def unload_extensions(ctx, *, extensions: str):
        embed = ExtensionManager.manage(bot, extensions.split(),
                action=ExtensionManager.UNLOAD, return_as_embed=True)

        await standard_send(ctx.channel, embed=embed)


    @bot.command(name='reload-extensions')
    @is_maintainer()
    async def reload_extensions(ctx, *, extensions: str):
        embed = ExtensionManager.manage(bot, extensions.split(),
                action=ExtensionManager.RELOAD, return_as_embed=True)

        await standard_send(ctx.channel, embed=embed)


    slash = SlashCommand(bot, sync_commands=True,
            sync_on_cog_reload=True, override_type=True)

    bot.run()
