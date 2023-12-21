# This doc is used for the help command on the discord bot.
from typing import List

import discord.ext.commands
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

# txt_help_help = """
# ```md
# ### Bot commands commands
# lobby           Returns the lobby of the user. A discord user can be mentioned to return their lobby. If the short link (shlink) functionality is enabled on the bot, the lobby link will be linked to a link shortener service and allow the users to click on the Steam link.
# profile         Returns the profile of the user and their active game. A discord user can be mentioned to return their profile.
# shlink          Behaves like the `lobby` command, but instead of returning "steam match link", returns the link shortener URL
#
# ### Account bindings
# link            Sets up your account providing the vanity url. If you need help setting it up use the command `help link`.
# unlink          Use this to unlink the account and will delete the database entry.
#
# ### Admin commands
# sync            Sync the commands with all the servers (Bot Owner only).
#
# ### Help commands
# help            Prints a list of commands and their description
# help link       How to link your Steam account with this bot.
# help lobby      How to use the lobby command (and shlink)
# help usage      Example on how to use this bot/Commands and stuff (sort of functionalities)
#
# ### Miscellany
# invite_bot       Returns a link to invite this bot to your server.
# botinvite       Returns a link to invite this bot to your server.
# version         Prints the current version of the bot
#
# ### Available Slash/App commands
# - help
# - link
# - lobby
# - profile
# - shlink
# - unlink
# ```
# > Note: To use Slash/Apps commands type `/` on the chat and proceed to select the desired command.
# """
#
# # **__Title:__**
# # help            Returns this list. This also has an alias `help general`
#
# zombie = """
# # Title
# """
#
# _text_test = {
#     "Bot commands commands":
#         """
#     ```
#     lobby           Returns the lobby of the user. A discord user can be mentioned to return their lobby. If the short link (shlink) functionality is enabled on the bot, the lobby link will be linked to a link shortener service and allow the users to click on the Steam link.
#     profile         Returns the profile of the user and their active game. A discord user can be mentioned to return their profile.
#     shlink          Behaves like the `lobby` command, but instead of returning "steam match link", returns the link shortener URL
#     ```
#     """,
#
#     "Account bindings":
#         """
#     ```
#     link            Sets up your account providing the vanity url. If you need help setting it up use the command `help link`.
#     unlink          Use this to unlink the account and will delete the database entry.
#     ```
#     """
# }
#
# _text_test2 = {
#     "Bot commands commands":
#         {
#             "lobby": "Returns the lobby of the user. A discord user can be mentioned to return their lobby. If the short link (shlink) functionality is enabled on the bot, the lobby link will be linked to a link shortener service and allow the users to click on the Steam link.",
#             "profile": "Returns the profile of the user and their active game. A discord user can be mentioned to return their profile.",
#             "shlink": 'Behaves like the `lobby` command, but instead of returning "steam match link", returns the link shortener URL',
#         }
#
# }

_help_commands = {
    ":tanabata_tree: __**Main Commands**__":
        [
            "lobby",
            "profile",
            "shlink",
        ],

    ":knot: __**Account bindings**__":
        [
            "link",
            "unlink"
        ],
    ":whale: __**Miscellany**__":
        [
            "invite_bot",
            "version"
        ],

}

_additional_commands = {
    ":hatching_chick: Help commands": {
        "help": "Prints a list of commands and their description",
        "help link": "How to link your Steam account with this bot.",
        "help lobby": "How to share a Steam lobby",
        "help profile": "How share a Steam profile",
        "help usage": "Example on how to use this bot/Commands and stuff (sort of functionalities)",
    }
}

_available_app_commands = ["help", "link", "lobby", "profile", "shlink", "unlink"]
_available_app_commands.sort()

txt_help_link = """
Using as reference my own Steam Account.

To obtain your vanity URL is as simple as going to your profile page, right click on the background and click "copy URL".

It should return something as the following:

`https://steamcommunity.com/id/SavageBidoof/`

Now we just need grab from that URL, the account name displayed.

Like: https://i.imgur.com/VHdVEj8.png

Once we have copied such part, we can proceed to linking the account with the `link` command.

Based on my Steam link, I would be using:

`s.link savagebidoof`

Note: This command is not sensitive to upper and lower case so write whatever you want.

Also, the prefix from the command I used might be different from the one running on this bot.

Couple images as reference (note that outputs and command prefix might vary):

https://i.imgur.com/jiYtPVN.png

https://i.imgur.com/7Ff5rzz.png

Regarding unlinking the account, the output will "always" be the same (as long it worked correctly).

As much there could be issues connecting to the database, in such scenario an error will be risen accordingly.

https://i.imgur.com/J7UUUPD.png
"""

txt_help_usage = """
```md
1. Link your Steam account to the Discord bot (doesn't require login nor authentication or anything like that), for more information about this step use the command `help link`.
2. Congrats you can now use the rest of commands, such as:
- Lobby
- Profile
- Shlink (if functionality enabled)
```

An image for reference, note that outputs and command prefix might vary (as well I would recommend to open the image on a new browser tab as otherwise might be blurry):
https://i.imgur.com/liZl6fI.png
"""

txt_help_lobby = """
The `lobby` command returns the Steam account of the user, their current active game, and their lobby (if there is one).

You can also target another user to display their lobby.

If the `shlink` (short links) functionality is enabled, links will be clickable and redirect towards the Steam lobby.


The `shlink` command does the same functionality as `lobby`, but the text displayed will be the short link, this is most useful if you wanna copy paste the short link to the lobby.

On both instances you can target another user to display their profile.

https://i.imgur.com/0D83hsz.png

https://i.imgur.com/BsjU1ps.png
"""

txt_help_profile = """
The `profile` command returns the Steam account of the user, and their current active game (if there is one).

You can also target another user to display their profile.

https://i.imgur.com/aVPfFzR.png
"""


# HELP_DIC = {
#     'general': txt_help_help,
#     'link': txt_help_link,
#     'lobby': txt_help_lobby,
#     'profile': txt_help_profile,
#     'usage': txt_help_usage,
# }


class HELPER:
    __HELPER_DIC: {str: Embed}
    __discord_bot: Bot

    def __init__(self, discord_bot: Bot):
        self.__HELP_DIC = {
            'general': lambda: self.general,
            'link': lambda: self.link,
            'lobby': lambda: self.lobby,
            'profile': lambda: self.profile,
            'usage': lambda: self.usage,
        }
        self.__discord_bot = discord_bot

    @property
    def menu_list(self) -> [str]:
        """
        Returns a list of the available menus (options extracted from the dictionary stored within this class)
        """
        return self.__HELP_DIC.keys()

    def menu(self, topic: str = None) -> [Embed]:
        embed_list: [Embed] = []
        if not topic:
            topic = 'general'
        topic = topic.lower()
        if topic not in self.__HELP_DIC:
            raise commands.errors.CommandNotFound
        _ = self.__HELP_DIC[topic]()
        if not isinstance(_, list):
            embed_list.append(_)
        else:
            for _embed in _:
                embed_list.append(_embed)
        return embed_list

    def __return_embed_template(self, title: str = "", description: str = "") -> Embed:
        embed = Embed(title=title, description=description, url="https://github.com/OriolFilter", color=0x7d3dd1)
        embed.set_author(name=self.__discord_bot.user.display_name, icon_url=self.__discord_bot.user.display_avatar)
        # embed.set_footer(text="https://github.com/OriolFilter")
        return embed

    @property
    def __return_embed_image_template(self) -> Embed:
        embed = Embed(title="", description="", url="https://github.com/OriolFilter", color=0x7d3dd1)
        return embed

    @property
    def general(self) -> Embed:
        return self._general()

    def _general(self) -> Embed:
        embed = self.__return_embed_template()
        # Add main commands
        for _topic, _command_list in _help_commands.items():
            _command_list.sort()
            _txt = "‎\n"
            for _command in _command_list:
                __command = self.__discord_bot.all_commands[_command]
                if not __command.hidden:
                    _txt += f"**{self.__discord_bot.command_prefix}{__command.name}:**         {__command.description}\n"
            _txt += "‎\n"
            embed.add_field(name=f"‎\n{_topic}", value=_txt, inline=False)

        ## Add list of extra help commands
        for _topic, _command_list in _additional_commands.items():
            _txt = "‎\n"
            for _command, _description in _command_list.items():
                _txt += f"**{self.__discord_bot.command_prefix}{_command}:**         {_description}\n"
            _txt += "‎\n"
            embed.add_field(name=f"‎\n{_topic}", value=_txt, inline=False)

        ## Add List of available thingies
        _txt = "‎\n"
        for _command in _available_app_commands:
            __command = self.__discord_bot.all_commands[_command]
            if not __command.hidden:
                _txt += f"- **{__command.name}**\n"
        embed.add_field(name="‎\n‎\n:bat: Available app/slash commands:", value=_txt, inline=False)
        return embed

    @property
    def profile(self) -> Embed:
        return self._profile()

    def _profile(self) -> Embed:
        embed_list = []
        embed = self.__return_embed_template()
        embed_list.append(embed)
        txt = (f"The `{self.__discord_bot.command_prefix}profile` command returns the Steam account of the user, "
               f"and their current active game (if there is one).\n\nYou can also target another user to display "
               f"their profile.")

        embed.add_field(name="", value=txt)
        images = ["https://i.imgur.com/aVPfFzR.png"]
        for _image_url in images:
            _embed = self.__return_embed_image_template
            _embed.set_image(url=_image_url)
            embed_list.append(_embed)
        return embed_list

    @property
    def usage(self) -> Embed:
        return self._usage()

    def _usage(self) -> list[Embed]:
        embed_list = []
        embed = self.__return_embed_template()
        embed_list.append(embed)
# 1. Link your Steam account to the Discord bot (doesn't require login nor authentication or anything like that), for more information about this step use the command `{self.__discord_bot.command_prefix}help link`.
        txt = f"""
```md
1. Link your Steam account using your Vanity URL (no password nor authentication used). Use `{self.__discord_bot.command_prefix}help link` for more information.

2. Congrats you can now use the rest of commands, such as:
- Lobby
- Profile
- Shlink
```
"""
        # txt1=f"1. Link your Steam account using your Vanity URL (no password nor authentication used). Use `{self.__discord_bot.command_prefix}help link` for more information."
        # txt2="2. Congrats you can now use the rest of commands, such as:\n* Lobby\n* Profile\n* Shlink"
        # embed.add_field(name="", value=txt1, inline=False)
        embed.add_field(name="", value=txt, inline=False)
        # embed.add_field(name="", value=txt, inline=False)
        images = ["https://i.imgur.com/pfSHgHL.png", "https://i.imgur.com/TULszNQ.png"]
        # images = []
        for _image_url in images:
            _embed = self.__return_embed_image_template
            _embed.set_image(url=_image_url)
            embed_list.append(_embed)
        return embed_list

    @property
    def lobby(self) -> Embed:
        return self._lobby

    @property
    def _lobby(self) -> Embed:
        embed_list = []
        embed = self.__return_embed_template()
        embed_list.append(embed)
        # The `lobby` command returns the Steam account of the user, their current active game, and their lobby (if there is one).
        # **{self.__discord_bot.command_prefix}lobby**: Post a link  to the lobby (if one is open)
        #
        # **{self.__discord_bot.command_prefix}shlink**: Post a link  to the lobby (if one is open), the link is shorten.
        txt = f"Use commands such **{self.__discord_bot.command_prefix}lobby** or **{self.__discord_bot.command_prefix}shlink** to post a lobby.\n\nYou can select another user to post their lobby."

        embed.add_field(name="", value=txt, inline=False)
        images = ["https://i.imgur.com/BsjU1ps.png", "https://i.imgur.com/0D83hsz.png"]
        for _image_url in images:
            _embed = self.__return_embed_image_template
            _embed.set_image(url=_image_url)
            embed_list.append(_embed)
        return embed_list

    @property
    def link(self) -> Embed:
        return self._link

    @property
    def _link(self) -> Embed:
        embed_list = []
        embed = self.__return_embed_template()
        embed_list.append(embed)

        text = f"""
            To get the `vanity URL` from your Steam account, go to your profile page, right click on the background and click **copy URL**.
            
            You should have copied something like this:
            
              `https://steamcommunity.com/id/SavageBidoof/`
                
            From that URL, the vanity URL is `SavageBidoof`.
                    
            Now you just need to use the link command appending the Steam vanity URL:
            
              `{self.__discord_bot.command_prefix}link savagebidoof`
            
            To unlink the account you can use the command `{self.__discord_bot.command_prefix}unlink`
            """

        embed.add_field(name="", value=text, inline=False)
        images = ["https://i.imgur.com/VHdVEj8.png", "https://i.imgur.com/7Ff5rzz.png",
                  "https://i.imgur.com/KQfOKgt.png"]

        for _image_url in images:
            _embed = self.__return_embed_image_template
            _embed.set_image(url=_image_url)
            embed_list.append(_embed)
        return embed_list
