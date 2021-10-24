#!/usr/bin/env python3

from discord_slash import SlashCommand
import discord
from aioconsole import ainput
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound, NoEntryPointError, ExtensionNotLoaded, ExtensionAlreadyLoaded


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

    async def on_ready(self):
        print('{0} is online'.format(self.user))

        while True:
            x = await ainput("> ")
            x = x.strip().split()
            if len(x) == 0:
                continue
            x = list(map(lambda x: x.strip(), x))
            try:
                if x[0] == "reload":
                    print("attempting to reload extension {0}".format(x[1]))
                    self.reload_cog(x[1])
                if x[0] == "unload":
                    print("attempting to unload extension {0}".format(x[1]))
                    self.unload_cog(x[1])
                if x[0] == "load":
                    print("attempting to load extension {0}".format(x[1]))
                    self.load_cog(x[1])
                elif x[0] == "quit":
                    import sys
                    sys.exit()
                else:
                    print('command not found')

            except IndexError:
                print('arguments not supplied')

    def get_token(self):
        """
        Check if the token file exists and if it does, return the
        contents after stripping leading and trailing whitespace.

        :return: The token
        :rtype: str
        """
        import os

        if not os.path.exists('token'):
            print(
                'token does not exist\ncreate a file called token with a discord token inside it')

        else:
            with open('token') as f:
                return f.read().strip()

    async def get_prefix(self, message) -> str:
        """
        This function can be modified later on for custom prefixes
        on a per server basis.

        :param discord.Message message: A message sent by a user
        :return: The custom prefix (at some point possibly)
        :rtype: str
        """
        return '!'

    def load_default_extensions(self) -> None:
        """
        Load the default extensions.
        """
        for extension in self._extensions:
            extension = 'cogs.{0}'.format(extension)
            self.load_cog(extension)

    def load_cog(self, cog_name: str) -> None:
        self.extension_error_handler(self.load_extension, cog_name, "load")

    def reload_cog(self, cog_name: str) -> None:

        self.extension_error_handler(self.reload_extension, cog_name, "reload")

    def unload_cog(self, cog_name: str) -> None:
        self.extension_error_handler(
            self.unload_extension, cog_name, "unload")

    def extension_error_handler(self, func, cog_name, load_ty: str):
        error_message = 'Failed to {1} extension: {0}'.format(
            cog_name, load_ty)

        try:
            func(cog_name)
            print('Successfully {1}ed extension: {0}'.format(
                cog_name, load_ty))

        except ExtensionNotFound:
            print(error_message)
            print('Are you sure this extension exists?')

        except NoEntryPointError:
            print(error_message)
            print('Are you sure this extension has a setup() method?')

        except ExtensionNotLoaded:
            print(error_message)
            print('Are you sure this extension has been loaded?')

    def run(self):
        """
        Run the bot if and only if the token file exists.
        """
        token = self.get_token()

        if token is not None:
            super().run(token.strip())


def main():
    bot = Bot()
    slash = SlashCommand(bot, sync_commands=True,
                         sync_on_cog_reload=True, override_type=True)
    bot.run()


if __name__ == '__main__':
    main()
