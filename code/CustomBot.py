import os
from typing import List

import DBClient
import Errors
import Steam
import discord

from psycopg2 import errors as DBErrors
from psycopg2 import OperationalError

from discord import Embed
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.context import Context

from functools import wraps

from Middleware import Middleware
from Classes import DiscordConf

from Steam import PlayerSummary

from Help import HELP_DIC

## Main

middleware: Middleware = Middleware()


# https://www.reddit.com/r/Discord_Bots/comments/nbnudq/multiple_optional_arguments_discordpy/
# https://discord.com/developers/docs/interactions/application-commands
# https://discord-py-slash-command.readthedocs.io/en/latest/quickstart.html#modals
# Move help to embed eventually


class CustomBot(commands.Bot):
    configuration: DiscordConf

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

    def __init__(self, *args, **kwargs):
        self.configuration = DiscordConf()
        intents = discord.Intents.default()
        intents.message_content = True
        super(commands.Bot, self).__init__(command_prefix=self.configuration.prefix,
                                           description=self.configuration.description,
                                           self_bot=False, intents=intents, help_command=None)
        self.add_commands()

    async def on_command_error(self, ctx: Context, exception: Exception):
        # discord.ext.commands.errors.MissingRequiredArgument
        # discord.ext.commands.errors.MissingRequiredArgument
        _: {Exception: Embed} = {
            DBErrors.NoDataFound: lambda: self._embed_error_no_steam_id_set,
            DBClient.DBSteamIDNotFoundError: lambda: self._embed_error_no_steam_id_set,
            commands.errors.CommandNotFound: lambda: self._embed_error_command_not_found,
            OperationalError: lambda: self._embed_error_no_db_connection,

        }

        if hasattr(exception, "original"):
            original_err_class = exception.original
        else:
            original_err_class = exception
        print(
            f'[ERROR] USER: {ctx.author.name} raised error {exception.__class__}\n\tWith line: {exception}')
        embed = None
        for key, value in _.items():
            if isinstance(original_err_class, key):
                embed = value
        if embed:
            await ctx.reply(embed=embed(), mention_author=True)
        else:
            print(f'Caught error {original_err_class}')
            await ctx.reply("Unknown error, contact the administrator.", mention_author=True)

    def run(self, *args, **kwargs):
        super(commands.Bot, self).run(self.configuration.token, *args, **kwargs)

    def is_god(self):
        async def extended_check(ctx: Context) -> bool:
            if int(ctx.author.id) != int(self.configuration.god_id):
                raise Errors.DiscordNotGodError()
            return True

        return commands.check(extended_check)

    def add_commands(self):
        @self.hybrid_command(name="help")
        async def help(ctx: Context, topic: str = None):
            """
            Use this command to display a list of options available and more!
            """
            # print(option)
            if topic is None:
                topic = 'general'
            if topic not in HELP_DIC:
                raise commands.errors.CommandNotFound
            await ctx.reply(HELP_DIC[topic], mention_author=False)

        @help.autocomplete('topic')
        async def help_autocomplete(
                ctx: Context,
                input: str,
        ) -> List[app_commands.Choice[str]]:
            topic_list = ['general', 'link', 'lobby', 'profile', 'usage']
            return [
                app_commands.Choice(name=topic, value=topic)
                for topic in topic_list if input.lower() in topic.lower()
            ]

        # @help.autocomplete('option')
        # @help.
        # async def help_autocomplete(
        #         ctx,
        #         current: str,
        # ) -> List[app_commands.Choice[str]]:
        #     options = ['links', 'usage']
        #     return [
        #         app_commands.Choice(name=option, value=option)
        #         for option in options if current.lower() in option.lower()
        #     ]
        #
        # @help.command(name="link")
        # async def help_link(ctx: Context):
        #     await ctx.reply(txt_help_link, mention_author=False)
        #
        # @help.command(name="usage")
        # async def help_usage(ctx: Context):
        #     await ctx.reply(txt_help_usage, mention_author=False)

        # @self.tree.command()
        # @self.hybrid_command()
        # async def fruits(interaction: discord.Interaction, fruit: str=None):
        #     await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')
        #
        # @fruits.autocomplete('fruit')
        # async def fruits_autocomplete(
        #         interaction: discord.Interaction,
        #         current: str,
        # ) -> List[app_commands.Choice[str]]:
        #     fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        #     return [
        #         app_commands.Choice(name=fruit, value=fruit)
        #         for fruit in fruits if current.lower() in fruit.lower()
        #     ]

        @self.command()
        @self.is_god()
        async def sync(ctx: Context):
            await self.tree.sync()
            await ctx.send("Sync!\nYou might need to reload the browser page or discord app for changes to be applied.")


        @self.command()
        async def botinvite(ctx: Context):
            """
            In case someone wants to add this bot to their server use the link provided by this command
            :param ctx:
            :return:
            """
            await ctx.reply(
                f'https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=84032&scope=bot',
                mention_author=False)

        @self.hybrid_command()
        async def link(ctx: Context, vanity_url: str=None):
            # https://discord-py-slash-command.readthedocs.io/en/latest/quickstart.html#modals?
            """
            Sets up your account providing the vanity url
            :param ctx:
            :param vanity_url:
            :return:
            """
            if not vanity_url:
                await ctx.reply(
                    f"You need to insert a vanity url, for further information regarding it's usage type '{self.command_prefix}vanity'.\nRemember that linking another account will overwrite the current linked one.")
            else:
                try:
                    steam_id = middleware.SteamApi.get_id_from_vanity_url(vanity_url)
                    middleware.set_steam_id(discord_id=ctx.author.id,
                                            steam_id=steam_id)
                    await ctx.reply(f"Just linked up your account, please verify that the account is correctly linked "
                                    f"by using the command `{self.command_prefix}profile`",
                                    mention_author=False)
                except Errors.VanityUrlNotFoundError:
                    await ctx.reply("Vanity URL couldn't be found, please check the syntax again, or use the command `help link` if you need guidance", mention_author=False)

        @self.hybrid_command()
        async def unlink(ctx: Context):
            """
            Use this to unlink the account.
            :return:
            """
            middleware.unset_steam_id(discord_id=ctx.author.id)
            await ctx.reply(
                "Successfully removed the entry (if there was one), please verify that the account is correctly unlinked "
                f"by using the command `{self.command_prefix}profile`", mention_author=False)

        @self.hybrid_command()
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

            steam_id = middleware.get_steam_id_from_discord_id(target_discord_id)
            summary = middleware.get_steam_summary(steam_id=steam_id)
            embed = self._embed_player_profile(summary)
            await ctx.send(embed=embed)

        # async def lobby(ctx: Context, member: Optional[discord.Member] = None):
        # @self.hybrid_command()
        @self.hybrid_command()
        async def lobby(ctx: Context, user: discord.User = None):
            """
            If no user is specified, posts the caller lobby in the chat.
            If a user is specified, it will apply the command `lobby` to them.
            :param ctx:
            :arg: Target user
            :return:
            """
            target_discord_id: int
            if user:
                target_discord_id = user.id
            else:
                target_discord_id = ctx.author.id

            steam_id = middleware.get_steam_id_from_discord_id(target_discord_id)
            summary = middleware.get_steam_summary(steam_id=steam_id)

            if not summary.has_lobby:
                embed = self._embed_error_no_lobby(summary)
                await ctx.reply("The account doesn't have an open lobby!", embed=embed, mention_author=True)
            else:
                embed = self._embed_player_lobby(summary)
                await ctx.reply(embed=embed, mention_author=False)
                # if not any(members):
                #     await ctx.reply(embed=embed, mention_author=False)
                # elif len(members) > 8:
                #     await ctx.reply("Sorry, max allowed players to invite are 8", mention_author=True)
                # else:
                #     mail_list = []
                #     for member in list(set(members)):
                #         if isinstance(member, discord.Member):
                #             mail_list.append(member)
                #         else:
                #             await ctx.reply(
                #                 "There was an error with the users given, ensure you @ed correctly the users ",
                #                 mention_author=True)
                #     for member in mail_list:
                #         await member.send(embed=embed)
                #     await ctx.reply("Sent an invite to the specified user(s)!", mention_author=False)

        @self.hybrid_command()
        async def shlink(ctx: Context, user: discord.User = None):
            # Add cooldown
            """
            Stands for "short link"
            Same as `lobby` command, but will return the link shortener as text instead of the lobby url. Only works if the `shortener` functionality is enabled.
            """

            if not middleware.ShlinkClient.enabled:
                return ctx.reply(embed=self._embed_shlink_not_enabled())
            else:
                target_discord_id: int
                if user:
                    target_discord_id = user.id
                else:
                    target_discord_id = ctx.author.id

                steam_id = middleware.get_steam_id_from_discord_id(target_discord_id)
                summary = middleware.get_steam_summary(steam_id=steam_id)

                if not summary.has_lobby:
                    embed = self._embed_error_no_lobby(summary)
                    await ctx.reply("The account doesn't have an open lobby!", embed=embed, mention_author=True)
                else:
                    embed = self._embed_player_lobby(summary)
                    await ctx.reply(embed=embed, mention_author=False)

        # @self.command()
        # async def vanity(ctx: Context):
        #     """
        #     How to use the link command, and from where to extract the vanity name
        #     :param ctx:
        #     :return:
        #     """
        #     await ctx.reply(f"ie:  `{self.command_prefix}link SavageBidoof`\nhttps://i.imgur.com/VHdVEj8.png",
        #                     mention_author=False)

        @self.command()
        async def version(ctx: Context):
            """
            Prints the current version
            :param ctx:
            :return:
            """
            await ctx.reply(embed=self._embed_version, mention_author=False)

        # @self.hybrid_command()
        # async def howto(ctx: Context):
        #     """
        #     Example on hot to use this bot
        #     """
        #     await ctx.reply("Use the following image as reference, note that the prefix command might "
        #                     "vary. (Also, open the image on the browser for better "
        #                     "clarity...)\nhttps://i.imgur.com/liZl6fI.png")

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
        embed.add_field(name="Version", value=f'v{os.getenv("VERSION")}', inline=True)
        # embed.add_field(name="Build Date", value=f'{os.getenv("BUILDDATE", "Unknown")}', inline=True)
        embed.set_footer(text=os.getenv("REPOSITORY"))
        return embed

    @property
    def _embed_error_command_not_found(self) -> Embed:
        """
        Embed used to tell the user command not found.
        :return:
        """
        # Be able to enable/disable on the guild
        # embed = Embed(title="Error", description="Specified Command not found", color=0xff5c5c)
        embed = Embed(title=f"Command not found!\nUse {self.command_prefix}help to get a list of available commands!")
        return embed

    @property
    def _embed_error_no_steam_id_set(self) -> Embed:
        """
        Embed that has a message indicating that the user has no steam_id currently linked
        :return:
        """
        embed = Embed(title="Error",
                      description=f"The discord user currently has no SteamID configured, to add an account use {self.command_prefix}link <vanity_url>",
                      color=0xff5c5c)
        embed.add_field(name=f"What is a vanity url?",
                        value=f"To learn more regarding the vanity rul, use: `{self.command_prefix}vanity`")
        embed.set_footer(text="https://github.com/OriolFilter")
        return embed

    @property
    def _embed_error_no_db_connection(self):
        """
        Embed used when cannot communicate to the database
        :return:
        """
        embed = Embed(title="Error",
                      description=f"Cannot communicate to the database, contact an administrator.",
                      color=0xff5c5c)
        embed.set_footer(text="https://github.com/OriolFilter")
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
            embed.add_field(name="User currently is not playing a game.", value=("Note that profile privacy settings "
                                                                                 "could be interfering with this."))

        embed.set_footer(text="https://github.com/OriolFilter")
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

    def _embed_error_no_lobby(self, player_summary: PlayerSummary) -> Embed:
        """
        This will be called ONLY after confirming if the user has or not has an available public lobby.

        Outside of this function, it will not be checked whether the user is playing something or not.
        """

        embed = Embed(title=f'{player_summary.personaname} Steam Profile', url=player_summary.profileurl,
                      color=self.__return_embed_color(player_summary=player_summary))

        embed.set_author(name=player_summary.personaname, url=player_summary.profileurl,
                         icon_url=player_summary.avatarfull)

        if player_summary.is_playing:

            game_title = player_summary.gameextrainfo

            embed.add_field(name="Currently playing:",
                            value=f'[{game_title}](https://store.steampowered.com/app/{player_summary.gameid})',
                            inline=False)

            embed.add_field(name="Public lobby currently not available",
                            value=f'Note that profile privacy settings or visibility could be interfering with this.',
                            inline=False)

            embed.set_thumbnail(
                url=f'https://cdn.cloudflare.steamstatic.com/steam/apps/{player_summary.gameid}/capsule_231x87.jpg')

        else:
            embed.add_field(name="User currently is not playing a game.",
                            value=("Note that profile privacy settings or visibility "
                                   "could be interfering with this."), inline=False)

        embed.set_footer(text="https://github.com/OriolFilter")
        return embed

    def _embed_player_lobby(self, player_summary: PlayerSummary) -> Embed:
        """
         This will be called ONLY after confirming the user has an available public lobby.

         This function won't check for anything of that.
         """
        shortLobbyUrl = ""
        message_lobby_url = ""

        if middleware.ShlinkClient.enabled:
            try:
                shortLobbyUrl = middleware.ShlinkClient.shorten(longurl=player_summary.lobby_url)
            except Errors.ShlinkError:
                print(f"Failed generating a short link for URL: {player_summary.lobby_url}")
            else:
                print(f"Some error occurred while generating a short link for URL: {player_summary.lobby_url}")

        embed = Embed(title=player_summary.gameextrainfo,
                      url=f'https://store.steampowered.com/app/{player_summary.gameid}',
                      color=self.__return_embed_color(player_summary=player_summary))

        embed.set_author(name=player_summary.personaname, url=player_summary.profileurl,
                         icon_url=player_summary.avatarfull)

        print(f">>> {shortLobbyUrl}")
        if shortLobbyUrl:
            message_lobby_url = f'[{player_summary.lobby_url}]({shortLobbyUrl})'
        else:
            message_lobby_url = player_summary.lobby_url
        print(f">>> {message_lobby_url}")

        embed.set_thumbnail(
            url=f'https://cdn.cloudflare.steamstatic.com/steam/apps/{player_summary.gameid}/capsule_231x87.jpg')
        embed.add_field(name=f'{player_summary.personaname}\'s lobby', value=message_lobby_url, inline=False)
        embed.set_footer(text="https://github.com/OriolFilter")
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

    def _embed_player_lobby_shlink(self, player_summary: PlayerSummary) -> Embed:
        """
        Exactly the same as `_embed_player_lobby`, but will return the shlink URL instead of the lobby URL (as in text)
        This won't validate if the link shortener is enabled.
        """

        shortLobbyUrl = middleware.ShlinkClient.shorten(longurl=player_summary.lobby_url)

        embed = Embed(title=player_summary.gameextrainfo,
                      url=f'https://store.steampowered.com/app/{player_summary.gameid}',
                      color=self.__return_embed_color(player_summary=player_summary))

        embed.set_author(name=player_summary.personaname, url=player_summary.profileurl,
                         icon_url=player_summary.avatarfull)

        embed.set_thumbnail(
            url=f'https://cdn.cloudflare.steamstatic.com/steam/apps/{player_summary.gameid}/capsule_231x87.jpg')
        embed.add_field(name=f'{player_summary.personaname}\'s lobby', value=shortLobbyUrl, inline=False)
        embed.set_footer(text=os.getenv("REPOSITORY"))
        return embed
