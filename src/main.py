#!/usr/bin/env python3

import discord

from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, NoEntryPointError

class Bot(commands.Bot):
    # default extensions
    _extensions = (
        'template',
    )

    def __init__(self):
        """
        Create an instance of Bot after setting intents, command_prefix
        and loading the default cogs.
        """
        super().__init__(intents=discord.Intents.all(),
                command_prefix=self.get_prefix)

        self.load_default_extensions()


    def get_token(self):
        """
        Check if the token file exists and if it does, return the
        contents after stripping leading and trailing whitespace.

        :return: The token
        :rtype: str
        """
        import os

        if not os.path.exists('token'):
            print('token does not exist\ncreate a file called token with a discord token inside it')

        else:
            with open('token') as f:
                return f.read().strip()


    async def get_prefix(self, message):
        """
        This function can be modified later on for custom prefixes
        on a per server basis.

        :param discord.Message message: A message sent by a user
        :return: The custom prefix (at some point possibly)
        :rtype: str
        """
        return '!'


    def load_default_extensions(self):
        """
        Load the default extensions.
        """
        for extension in self._extensions:
            extension = 'cogs.{0}'.format(extension)

            try:
                self.load_extension(extension)
                print('Successfully loaded extension: {0}'.format(extension))

            except ExtensionNotFound:
                print('Failed to load extension: {0}'.format(extension))
                print('Are you sure this extension exists?')

            except NoEntryPointError:
                print('Failed to load extension: {0}'.format(extension))
                print('Are you sure this extension has a setup() method?')


    def run(self):
        """
        Run the bot if and only if the token file exists.
        """
        token = self.get_token()

        if token is not None:
            super().run(token.strip())


if __name__ == '__main__':
    bot = Bot()
    bot.run()
