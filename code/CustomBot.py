import os
from functools import wraps

import discord
from discord.ext import commands
from discord import Embed
from discord.ext.commands.context import Context

import Steam
from Middleware import Middleware
from Classes import DiscordConf
from psycopg2 import errors as dberrors
from psycopg2 import OperationalError
from Steam import PlayerSummary
import DBClient

middleware = Middleware()

class CustomBot(commands.Bot):
    configuration: DiscordConf

    async def on_ready(self):
        print('------')
        print('Logged as')
        print(self.user.name)
        print(self.user.id)
        print(
            f'invite me with: https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=84032&scope=bot')
        print('------')

    def __init__(self, *args, **kwargs):
        self.configuration = DiscordConf()
        super(commands.Bot, self).__init__(command_prefix=self.configuration.prefix,
                                           description=self.configuration.description,
                                           self_bot=False)
        self.add_commands()

    async def on_command_error(self, ctx: Context, exception: Exception):
        _: {Exception: Embed} = {
            dberrors.NoDataFound: lambda: self._embed_error_no_steam_id_set,
            DBClient.DBSteamIDNotFoundError: lambda: self._embed_error_no_steam_id_set,
            commands.errors.CommandNotFound: lambda: self._embed_error_command_not_found
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
            await ctx.send(embed=embed())
        else:
            await ctx.send("Unknown error, contact the administrator.")

    def run(self, *args, **kwargs):
        super(commands.Bot, self).run(self.configuration.token, *args, **kwargs)

    def add_commands(self):
        @self.command()
        async def discord_invite(ctx):
            """
            In case someone wants to add this bot to their server use the link provided by this command
            :param ctx:
            :return:
            """
            await ctx.send(
                f'https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=84032&scope=bot))')

        @self.command()
        async def link(ctx: Context, vanity_url: str = None):
            """
            Sets up your account providing the vanity url
            :param ctx:
            :param vanity_url:
            :return:
            """
            if not vanity_url:
                await ctx.send(
                    f"You need to insert a vanity url, for further information uppon it's usage type '{self.command_prefix}help' (not added yet)")
            else:
                try:
                    steam_id = middleware.SteamApi.get_id_from_vanity_url(vanity_url)
                    middleware.set_steam_id(discord_id=ctx.author.id,
                                            steam_id=steam_id)
                    await ctx.send(f"Just linked up your account, please verify the following account is "
                                   f"yours.\nhttps://www.steamidfinder.com/signature/{steam_id}.png")
                except Steam.VanityUrlNotFound:
                    await ctx.send("Vanity URL couldn't be found, please check the syntax again")

        @self.command()
        async def unlink(ctx):
            """
            Use this to unlink the account.
            :return:
            """
            middleware.unset_steam_id(discord_id=ctx.author.id)
            await ctx.send("Successfully removed the entry")

        @self.command()
        async def status(ctx: Context, user: discord.User = None):
            """
            Placeholder, it does be mad ugly
            Returns the status of the specified player
            :param ctx:
            :param user:
            :return:
            """
            if user:
                steam_id = middleware.get_steam_id_from_discord_id(user.id)
            else:
                steam_id = middleware.get_steam_id_from_discord_id(ctx.author.id)
            summary = middleware.get_steam_summary(steam_id=steam_id)
            embed = self._embed_simple_player(summary)
            await ctx.send(embed=embed)

        @self.command()
        async def lobby(ctx: Context, *members: discord.Member):
            # Add cooldown
            """
            If no user is specified, posts the caller lobby in the chat, if users are specified sends the lobby url
            to the specified user(s) DM's
            :param ctx:
            :arg: List of users
            :return:
            """
            steam_id = middleware.get_steam_id_from_discord_id(ctx.author.id)
            summary = middleware.get_steam_summary(steam_id=steam_id)
            if summary.has_lobby:
                embed = self._embed_player_lobby(summary)
            else:
                embed = self._embed_error_no_lobby(summary)

            if not any(members):
                await ctx.send(embed=embed)
            elif len(members) > 4:
                await ctx.send("Sorry, max allowed players to invite are 4")
            else:
                mail_list = []
                for member in list(set(members)):
                    if isinstance(member, discord.Member):
                        mail_list.append(member)
                    else:
                        await ctx.send("There was an error with the users given, ensure you @ed correctly the users ")
                for member in mail_list:
                    await member.send(embed=embed)
                await ctx.send("Sent an invite to the specified user(s)!")

        @self.command()
        async def vanity(ctx: Context):
            """
            How to use the link command, and from where to extract the vanity name
            :param ctx:
            :return:
            """
            await ctx.send(f"ie:  `{self.command_prefix}link SavageBidoof`\nhttps://i.imgur.com/VHdVEj8.png")

        @self.command()
        async def profile(ctx: Context, user: discord.User = None):
            """
            Show your profile
            :param ctx:
            :param user:
            :return:
            """
            if user:
                steam_id = middleware.get_steam_id_from_discord_id(user.id)
            else:
                steam_id = middleware.get_steam_id_from_discord_id(ctx.author.id)
            await ctx.send(f'https://www.steamidfinder.com/signature/{steam_id}.png')

        @self.command()
        async def version(ctx:Context):
            """
            Prints the current version and the github container
            :param ctx:
            :return:
            """
            repo="https://github.com/OriolFilter/Steam_Invite_Discord"
            vers=os.getenv("VERSION")
            await ctx.send(f"Current version: {vers}\nOG Repository:\n{repo}")

            # await ctx.send(embed=embed)

    @property
    def _embed_error_command_not_found(self) -> Embed:
        """
        Embed used to tell the user command not found.
        :return:
        """
        # Be able to enable/disable on the guild
        return Embed(title="Command not found placeholder.")
        # return None

    @property
    def _embed_error_no_steam_id_set(self) -> Embed:
        """
        Embed that has a message indicating that the user has no steam_id currently linked
        :return:
        """
        embed = Embed(title="Error",
                      description=f"The discord user currently has no SteamID configured, to add an account use {self.command_prefix}link <vanity_url>",
                      color=0xff5c5c)
        embed.set_footer(text=f"use {self.command_prefix}vanity for more information regarding what is vanity url")
        embed.set_footer(text="https://github.com/OriolFilter")
        return embed

    # def __generate_embed_summary_player(self, player_summary: PlayerSummary) -> Embed:
    #     embed = Embed(title=player_summary.personaname, url=player_summary.profileurl, color=0x61ff64)
    #     embed.set_thumbnail(url=player_summary.avatarfull,)
    #     return embed

    # def _embed_simple_player(self, player_summary: PlayerSummary) -> Embed:
    #     """
    #     Expand.
    #     :param player_summary:
    #     :return:
    #     """
    #     embed = Embed(title=player_summary.personaname, url=player_summary.profileurl, color=0x61ff64)
    #     embed.set_thumbnail(url=player_summary.avatarfull, )
    #     embed.set_footer(text="https://github.com/OriolFilter")
    #     return embed

    def _embed_simple_player(self, player_summary: PlayerSummary) -> Embed:
        """
        Expand.
        :param player_summary:
        :return:
        """
        embed = Embed(title=player_summary.personaname, url=player_summary.profileurl, color=0x61ff64)
        embed.set_thumbnail(url=player_summary.avatarfull, )
        embed.add_field(name="Currenty playing?", value=("No", "Yes")[player_summary.is_playing])
        embed.set_footer(text="https://github.com/OriolFilter")
        return embed

    def _embed_error_no_lobby(self, player_summary: PlayerSummary) -> Embed:
        embed = Embed(title=player_summary.personaname, url=player_summary.profileurl, color=0xfff261)
        embed.set_thumbnail(url=player_summary.avatarfull, )
        embed.add_field(name="User currently doesn't have an available lobby", value="--", inline=False)
        embed.add_field(name="Is user playing?",
                        value=f"Currently playing {player_summary.gameextrainfo}" if player_summary.gameextrainfo else "No")
        embed.set_footer(text="https://github.com/OriolFilter")
        return embed

    def _embed_player_lobby(self, player_summary: PlayerSummary) -> Embed:
        embed = Embed(title=player_summary.gameextrainfo,
                      url=f'https://store.steampowered.com/app/{player_summary.gameid}', color=0xffc766)
        embed.set_author(name=player_summary.personaname, url=player_summary.profileurl,
                         icon_url=player_summary.avatarfull)
        embed.set_thumbnail(
            url=f'https://cdn.cloudflare.steamstatic.com/steam/apps/{player_summary.gameid}/capsule_231x87.jpg')
        embed.add_field(name=f'{player_summary.personaname}\'s lobby', value=player_summary.lobby_url, inline=False)
        embed.set_footer(text="https://github.com/OriolFilter")
        return embed
