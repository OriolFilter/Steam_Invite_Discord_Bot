import os

from typing import List

import DBClient
import Errors

from psycopg2 import errors as DBErrors
from psycopg2 import OperationalError

import discord
from discord import Embed
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.context import Context

from Middleware import Middleware
from Classes import DiscordConf

from Steam import PlayerSummary

from Help import HELPER

## Main
middleware: Middleware = Middleware()


# https://discord.com/developers/docs/interactions/application-commands
# https://discord-py-slash-command.readthedocs.io/en/latest/quickstart.html#modals
# Move help to embed eventually


class CustomBot(commands.Bot):
    configuration: DiscordConf
    helper_class: HELPER
    _link_menu_options: list[str]
    __connected: bool

    async def on_ready(self):
        print('------')
        print('Logged as')
        print(self.user.name)
        print(self.user.id)
        print(f'invite me with: {self.invite_url}')
        print('------')
        await self.change_presence(activity=discord.Game(
            name=(
                self.configuration.activity, f"Use {self.configuration.prefix}help to get a list "
                                             f"from all the available commands")[not any(self.configuration.activity)]
        ))

    @property
    def is_connected(self) -> bool:
        return self.__connected

    def _set_as_connected(self):
        self.__connected = True

    def _set_as_disconnected(self):
        self.__connected = False

    async def on_resumed(self):
        self._set_as_connected()
        print("Reconnected!")

    async def on_connect(self):
        self._set_as_connected()
        print("Connected!")

    async def on_disconnect(self):
        self._set_as_disconnected()
        print("Disconnected!")

    def __init__(self, *args, **kwargs):
        self.__connected = False
        self.configuration = DiscordConf()
        intents = discord.Intents.default()
        intents.message_content = True
        super(commands.Bot, self).__init__(command_prefix=self.configuration.prefix,
                                           # description=self.configuration.description,
                                           self_bot=False, intents=intents, help_command=None)
        self.helper_class = HELPER(discord_bot=self)
        self.add_commands()
        self._link_menu_options = ['steamid', 'vanity']

    async def on_command_error(self, ctx: Context, exception: Exception):
        """
        On command error "returns" an embed based on the exception risen.

        Object `_` contains is a dictionary that stores an embed for each one of the errors.

        By `return` I mean that prints back to the user.
        """
        # discord.ext.commands.errors.MissingRequiredArgument #Not used as per the moment
        # https://github.com/Rapptz/discord.py/discussions/8384
        _: {Exception: Embed} = {
            DBErrors.NoDataFound: lambda: self._embed_error_no_steam_id_set,
            DBClient.DBSteamIDNotFoundError: lambda: self._embed_error_no_steam_id_set,
            commands.errors.CommandNotFound: lambda: self._embed_error_command_not_found,
            OperationalError: lambda: self._embed_error_no_db_connection,
            Errors.VanityUrlNotFoundError: lambda: self._embed_error_vanity_url_not_found,
            Errors.SteamIdUserNotFoundError: lambda: self._embed_error_steam_id_not_found,
            Errors.DiscordNotGodError: lambda: self._embed_error_not_god_user,
            Errors.ShlinkNotEnabledError: lambda: self._embed_shlink_not_enabled,
        }

        raised_exception: Exception

        # when discord.ext.commands.errors.HybridCommandError is risen, I gotta digg 2 times down to get the error I raised (discord by itself hides it 2 layers deep)
        if isinstance(exception, discord.ext.commands.errors.HybridCommandError):
            _exception_layer1: Exception = exception.original
            _exception_layer2: Exception = _exception_layer1.original  # Desired target
            raised_exception = _exception_layer2
        else:
            raised_exception: Exception = exception

        if hasattr(raised_exception, "original"):
            original_err_class = raised_exception.original
        else:
            original_err_class = raised_exception
        print(
            f'[ERROR] USER: {ctx.author.name} raised error {raised_exception.__class__}\n\tWith line: {raised_exception}')
        embed = None
        for _key, _lambda_func in _.items():
            if isinstance(original_err_class, _key):
                embed = _lambda_func()
        if embed:
            await ctx.reply(embed=embed, mention_author=True)
        else:
            print(f'Caught error {original_err_class}')
            await ctx.reply("Unknown error, contact the administrator.", mention_author=True)

    async def run(self, *args, **kwargs):
        await self.start(token=self.configuration.token, reconnect=True)
        # super(commands.Bot, self).run(self.configuration.token, *args, **kwargs, reconnect=True)

    # def is_god(self):
    #     async def extended_check(ctx: Context) -> bool:
    #         if self.configuration.god_id and int(ctx.author.id) != int(self.configuration.god_id):
    #             raise Errors.DiscordNotGodError
    #         return True
    #
    #     return commands.check(extended_check)

    def add_commands(self):
        @self.hybrid_command(name="help", description="Prints a list of commands and their description")
        async def help(ctx: Context, topic: str = None):
            """
            Use this command to display a list of options available and more!
            """
            if not isinstance(ctx.channel, discord.channel.DMChannel):
                # _command = ctx.author.send
                await ctx.author.send(embeds=self.helper_class.menu(topic=topic), mention_author=False)
                await ctx.reply("DM sent!", mention_author=False)
            else:
                await ctx.reply(embeds=self.helper_class.menu(topic=topic), mention_author=False)

        @help.autocomplete('topic')
        async def help_autocomplete(ctx: Context, input: str, ) -> List[app_commands.Choice[str]]:
            topic_list = self.helper_class.menu_list
            return [
                app_commands.Choice(name=topic, value=topic)
                for topic in topic_list if input.lower() in topic.lower()
            ]

        @self.command(hidden=True, description="Sync the commands with all the servers (Bot Owner only).")
        # @self.is_god()
        async def sync(ctx: Context):
            """
            Syncs the slash/app commands with the discord servers (globaly)
            """
            if self.configuration.god_id and int(ctx.author.id) != int(self.configuration.god_id):
                raise Errors.DiscordNotGodError
            await self.tree.sync()
            await ctx.send("Sync!\nYou might need to reload the browser page or discord app for changes to be applied.")

        @self.command(description="Returns a link to invite this bot to your server.")
        # async def botinvite(ctx: Context):
        async def invite_bot(ctx: Context):
            """
            In case someone wants to add this bot to their server use the link provided by this command
            :param ctx:
            :return:
            """
            await ctx.reply(
                f'https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=84032&scope=bot',
                mention_author=False)

        # @self.hybrid_command(description=f"Links your steam account. Use **{self.command_prefix}help link** for help.")
        @self.hybrid_group(description=f"Links your steam account. Use **{self.command_prefix}help link** for help.",
                           hidden=True)
        async def link(ctx: Context, option: str = None, input: str = None):
            """
            Use this command to display a list of options available and more!
            """
            if ctx.invoked_subcommand is None:
                await ctx.reply(
                    f'You need to specify which method to link wanna use, either **{self.command_prefix} vanity <vanity url>** or **{self.command_prefix}link steamid <steam id>**.\nUse **{self.command_prefix}help link** to get help regarding how to link your account.')

        @link.command(description=f"Links your Steam account using your Steam vanity URL.")
        async def vanity(ctx: Context, vanity_url: str = None):
            if not vanity_url:
                await ctx.reply(
                    f"You need to insert a Steam vanity url, use `{self.command_prefix}help link` for help.\nRemember that linking another account will overwrite the current linked one.")
            else:
                steam_id = middleware.SteamApi.get_id_from_vanity_url(vanity_url)
                middleware.set_steam_id(discord_id=ctx.author.id,
                                        steam_id=steam_id)
                await ctx.reply("Just linked up your account, please verify that the account linked is correct.",
                                mention_author=False,
                                embed=self._profile(discord_id=ctx.author.id))

        # @link.command(description=f"Links your Steam account specifying your Steam account ID. Use **{self.command_prefix}help link** for help.")
        @link.command(description=f"Links your Steam account using your Steam account ID.")
        async def steamid(ctx: Context, steam_id: str = None):
            if not steam_id:
                await ctx.reply(
                    f"You need to insert a Steam account ID, use `{self.command_prefix}help link` for help.\nRemember that linking another account will overwrite the current linked one.")
            else:
                if middleware.SteamApi.player_summary(steam_id):
                    middleware.set_steam_id(discord_id=ctx.author.id, steam_id=steam_id)
                    await ctx.reply("Just linked up your account, please verify that the account linked is correct.",
                                    mention_author=False,
                                    embed=self._profile(discord_id=ctx.author.id))

        @self.hybrid_command(description="Unlink your Steam account.")
        # @self.hybrid_command(description="Use this to unlink the account and will delete the database entry.")
        async def unlink(ctx: Context):
            """
            Use this to unlink the account.
            :return:
            """
            middleware.unset_steam_id(discord_id=ctx.author.id)
            await ctx.reply(
                "Successfully removed the entry (if there was one), please verify that the account is correctly unlinked "
                f"by using the command `{self.command_prefix}profile`", mention_author=False)

        @self.hybrid_command(
            description=f"Posts profile of the user and their active game. Use **{self.command_prefix}help profile** for help.")
        async def profile(ctx: Context, user: discord.User = None):
            """
            Returns Steam account from the user and their current open game (if they are currently playing)
            :param ctx:
            :param user: User targeted on which the command "profile" will be used.
            :return:
            """
            target_discord_id: int
            if user:
                target_discord_id = user.id
            else:
                target_discord_id = ctx.author.id
            await ctx.send(embed=self._profile(discord_id=target_discord_id))

        @self.hybrid_command(
            description=f"Posts link to the lobby. Use **{self.command_prefix}help lobby** for help.")
        async def lobby(ctx: Context, user: discord.User = None):
            """

            """
            await self._lobby(ctx=ctx, user=user)

        @self.hybrid_command(
            description=f"Behaves like the **lobby** command. Returns a short link instead of a lobby link.")
        async def shlink(ctx: Context, user: discord.User = None):
            """
            Stands for "short link".
            Raise `ShlinkNotEnabledError` if Shlink functionality is enabled.
            """
            if not middleware.ShlinkClient.enabled:
                raise Errors.ShlinkNotEnabledError
            await self._lobby(ctx=ctx, user=user, shlink_as_text=True)

        @self.command(description="Prints the current version of the bot.")
        async def version(ctx: Context):
            """
            Prints the current version
            :param ctx:
            :return:
            """
            await ctx.reply(embed=self._embed_version, mention_author=False)

    @property
    def invite_url(self) -> str:
        return f"https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=84032&scope=bot"

    @property
    def _embed_version(self) -> Embed:
        """
        Returns an embed object with the GitHub Repo
        """
        embed = Embed(title="Github Repository", url=os.getenv("REPOSITORY"),
                      description="Discord bot intended to get lobby links from Steam users", color=0xababab)
        embed.set_author(name="OriolFilter", url="https://github.com/OriolFilter",
                         icon_url="https://avatars.githubusercontent.com/u/55088942?v=4")
        embed.add_field(name="Version", value=f'v{os.getenv("VERSION")}', inline=False)
        embed.add_field(name="Repository", value=f'{os.getenv("REPOSITORY")}', inline=False)
        # embed.add_field(name="Build Date", value=f'{os.getenv("BUILDDATE", "Unknown")}', inline=True)
        # embed.set_footer(text=os.getenv("REPOSITORY"))
        return embed

    def __return_embed_error_template(self, title: str, description: str) -> discord.Embed:
        embed = Embed(title=title, description=description, color=0xff5c5c)
        embed.set_footer(text="https://github.com/OriolFilter")
        return embed

    @property
    def _embed_error_command_not_found(self) -> Embed:
        """
        Embed used to tell the user command not found.
        :return:
        """
        return self.__return_embed_error_template(title="Command not found!",
                                                  description=f"Use `{self.command_prefix}help` to get a list of available commands!")

    @property
    def _embed_error_no_steam_id_set(self) -> Embed:
        """
        Embed that has a message indicating that the user has no steam_id currently linked
        :return:
        """
        embed = self.__return_embed_error_template(title="No SteamID currenlty linked",
                                                   description=f"The discord user currently has no SteamID configured, to add an account use `{self.command_prefix}link <vanity_url>`")
        embed.add_field(name=f"What is a vanity url?",
                        value=f"To learn more regarding the vanity rul, use: `{self.command_prefix}vanity`")
        return embed

    @property
    def _embed_error_no_db_connection(self):
        """
        Embed used when cannot communicate to the database
        :return:
        """
        embed = self.__return_embed_error_template(title="Cannot connect to the database",
                                                   description=f"Please contact an administrator to check the infrastructure status.")
        return embed

    @property
    def _embed_error_vanity_url_not_found(self):
        """
        Embed used when the user (Steam vanity URL) is not found.
        :return:
        """

        embed = self.__return_embed_error_template(title="Vanity URL not found",
                                                   description=f"Vanity URL didn't match an user, use the command `{self.command_prefix}help link` for help.")
        return embed

    @property
    def _embed_error_steam_id_not_found(self):
        """
        Embed used when the user (Steam vanity URL) is not found.
        :return:
        """

        embed = self.__return_embed_error_template(title="Steam ID not found",
                                                   description=f"Steam ID didn't match an user, use the command `{self.command_prefix}help link` for help.")
        return embed

    @property
    def _embed_error_not_god_user(self):
        """
        Embed used when the user is expected to be GOD (aka Bot Administrator), but it's not.
        :return:
        """
        embed = self.__return_embed_error_template(title="You are not GOD!.",
                                                   description=f"Only GOD is allowed to run this command.")
        return embed

    def _embed_player_profile(self, player_summary: PlayerSummary) -> Embed:
        """
        Generates the embed for the player profile command
        Embed color is picked based on the user activity
        :param player_summary:
        :return:
        """

        embed = Embed(title=f'{player_summary.personaname} Steam Profile', url=player_summary.profileurl,
                      color=self.__return_embed_color(player_summary=player_summary))

        embed.set_author(name=player_summary.personaname, url=player_summary.profileurl,
                         icon_url=player_summary.avatarfull)

        if player_summary.is_playing:
            game_title = player_summary.gameextrainfo
            if not game_title:
                print("player_summary.gameextrainfo value is set to none!")
                print(player_summary.__dict__())
            embed.add_field(name="Currently playing:",
                            value=f'[{game_title}](https://store.steampowered.com/app/{player_summary.gameid})')

            embed.set_thumbnail(
                url=f'https://cdn.cloudflare.steamstatic.com/steam/apps/{player_summary.gameid}/capsule_231x87.jpg')

        else:
            if player_summary.has_public_visibility:
                embed.add_field(name="User currently is not playing a game.", value="")
            else:
                embed.add_field(name="User activity not public",
                                value="Since the Steam account doesn't activity set to public, I cannot see if it's "
                                      "playing a game or not.")
        return embed

    @staticmethod
    def __return_embed_color(player_summary: PlayerSummary) -> hex:

        """
        Sets embed color based on current activity, and as well sets Title and Author fields + respective links to the Steam Account page.

        Those fields can be removed afterward.
        """

        embed_color: hex = 0x41ffe6

        if player_summary.has_lobby:
            embed_color = 0xff1abb
        elif player_summary.is_playing:
            embed_color = 0x61ff64

        return embed_color

    def _embed_player_lobby(self, player_summary: PlayerSummary, shlink_as_text: bool) -> Embed:
        """
         This will be called ONLY after confirming the user has an available public lobby.

         This function won't check for anything of that.
         """
        shortLobbyUrl: str = ""
        message_lobby_url: str
        if middleware.ShlinkClient.enabled:
            try:
                shortLobbyUrl = middleware.ShlinkClient.shorten(longurl=player_summary.lobby_url)
            except Errors.ShlinkError:
                print(f"Failed generating a short link for URL: {player_summary.lobby_url}")
            except Errors as e:
                print(f"Some error occurred while generating a short link for URL: {player_summary.lobby_url}")

        embed = Embed(title=player_summary.gameextrainfo,
                      url=f'https://store.steampowered.com/app/{player_summary.gameid}',
                      color=self.__return_embed_color(player_summary=player_summary))

        embed.set_author(name=player_summary.personaname, url=player_summary.profileurl,
                         icon_url=player_summary.avatarfull)

        if middleware.ShlinkClient.enabled and shlink_as_text and shortLobbyUrl:
            message_lobby_url = player_summary.lobby_url
        elif shortLobbyUrl:
            message_lobby_url = f'[{[player_summary.lobby_url, shortLobbyUrl][shlink_as_text]}]({shortLobbyUrl})'
        else:
            message_lobby_url = player_summary.lobby_url

        embed.set_thumbnail(
            url=f'https://cdn.cloudflare.steamstatic.com/steam/apps/{player_summary.gameid}/capsule_231x87.jpg')
        embed.add_field(name=f'{player_summary.personaname}\'s lobby', value=message_lobby_url, inline=False)
        return embed

    def _embed_shlink_not_enabled(self) -> Embed:
        """
        Returns a Discord Embed used to tell the user that shlink functionality is not enabled.
        """
        embed = Embed(title="Shlink functionality is not enabled", description="Link shortener (shlink) functionality "
                                                                               "is not enabled.\nReach out the bot "
                                                                               "administrator in case you would like "
                                                                               "for them to enable such.",
                      color=0x8a8a8a)
        return embed

    def _profile(self, discord_id: int) -> Embed:
        """
        Returns a profile embed for the discord ID specified
        :return Embed
        """
        steam_id = middleware.get_steam_id_from_discord_id(discord_id)
        summary = middleware.get_steam_summary(steam_id=steam_id)
        embed = self._embed_player_profile(summary)
        return embed

    async def _lobby(self, ctx: Context, user: discord.User = None, shlink_as_text=False):
        """
        This function unifies `lobby` and `shlink` commands.
        If no user is specified, uses the Steam account linked to the user that called this command.
        If a user is specified, it will target instead the user mentioned.
        If not a lobby available, will use the profile embed instead.
        """
        target_discord_id: int
        if user:
            target_discord_id = user.id
        else:
            target_discord_id = ctx.author.id

        steam_id = middleware.get_steam_id_from_discord_id(target_discord_id)
        summary = middleware.get_steam_summary(steam_id=steam_id)

        if summary.has_lobby:
            embed = [
                self._embed_player_profile(summary),
                self._embed_player_lobby(summary, shlink_as_text=shlink_as_text)
            ][summary.has_lobby]
        else:
            embed = self._embed_player_profile(summary)

        await ctx.reply(mention_author=False, embed=embed)
