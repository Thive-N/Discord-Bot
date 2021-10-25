import traceback

from discord.ext.commands.errors import ExtensionNotFound, \
        ExtensionAlreadyLoaded, ExtensionFailed, \
        ExtensionNotLoaded, NoEntryPointError

from utils.standard import StandardEmbed

class ExtensionManager:
    LOAD = 0
    UNLOAD = 1
    RELOAD = 2

    @staticmethod
    def manage(bot, extensions, action=LOAD, return_as_embed=False):
        """
        Manages dynamically loadable extensions for the bot.

        :param Bot bot: An instance of Bot
        :param list extensions: The extensions to manage
        :param int action: The action to take on said extensions
        :param bool return_as_embed: Whether to return an embed
        :return: failed and succeeded extensions or an embed
        :rtype: tuple, discord.Embed
        """

        if action < 0 or action > 2:
            print('Invalid action: {0}'.format(action))

        fail = 'Failed to load extension: {0}'

        func, success = (
            (bot.load_extension, 'Successfully loaded extension: {0}'),
            (bot.unload_extension, 'Successfully unloaded extension: {0}'),
            (bot.reload_extension, 'Successfully reloaded extension: {0}'),
        )[action]

        failed = list(extensions)
        succeeded = []

        for extension in extensions:
            try:
                func('cogs.{0}'.format(extension))
                print(success.format(extension))

            except ExtensionNotFound:
                print(fail.format(extension))
                print('Are you sure this extension exists?')

            except ExtensionAlreadyLoaded:
                print(fail.format(extension))
                print('Are you sure this extension is unloaded?')

            except ExtensionFailed as e:
                print(fail.format(extension))
                print('Are you sure this extension is programmed correctly?')
                traceback.print_exc()

            except ExtensionNotLoaded:
                print(fail.format(extension))
                print('Are you sure this extension is loaded?')

            except NoEntryPointError:
                print(fail.format(extension))
                print('Are you sure this extension has a setup() method?')

            else:
                failed.remove(extension)
                succeeded.append(extension)

        if return_as_embed is True:
            succeeded_str = ', '.join(succeeded)
            if succeeded_str == '':
                succeeded_str = 'N/A'

            failed_str = ', '.join(failed)
            if failed_str == '':
                failed_str = 'N/A'

            embed = StandardEmbed(bot, description='Extensions')
            embed.add_field(name='Succeeded', value=succeeded_str, inline=False)
            embed.add_field(name='Failed', value=failed_str, inline=False)

            return embed

        else:
            return failed, succeeded
