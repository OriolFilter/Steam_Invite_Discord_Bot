# This doc is used for the help command on the discord bot.
from dataclasses import dataclass
from typing import List

import discord.ext.commands
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

# {
#   "topic":
#   {
#      "command_with_subcommands": ["list", "of", "subcommands"],
#      "command_without_subcommand": []
#   },
#   "topic2":{}
# }

_help_commands_part1 = {
    ":tanabata_tree: __**Main Commands**__":
        [
            "lobby",
            "profile",
            "shlink",
        ],
    ":knot: __**Account bindings**__":
        [
            "link",
            "unlink",
        ],

}
_help_commands_part2 = {
    ":whale: __**Miscellany**__":
        [
            "invite_bot",
            "version"
        ],
}
# _miscellany_commands=[
#             "invite_bot",
#             "version"
#         ],

# _account_binding_commands = {
#     ":knot: __**Account bindings**__":
#         [
#             "link",
#             "unlink"
#         ],
# }

_additional_commands = {
    ":hatching_chick: Help commands": {
        "help": "Prints a list of commands and their description.",
        "help link": "How to link your Steam account with this bot.",
        "help lobby": "How to share a Steam lobby.",
        "help profile": "How share a Steam profile.",
        "help usage": "Example on how to use this bot/Commands and stuff (sort of functionalities).",
    }
}

_available_app_commands = ["help", "link", "lobby", "profile", "shlink", "unlink"]
_available_app_commands.sort()


@dataclass
class HELPER_LINK_SKEL:
    title: str
    text: str
    image_list: list[str]


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

    def _manage_help_commands_dictionary(self, help_commands_dictionary: _help_commands_part1 | _help_commands_part2,
                                         embed: Embed,
                                         end: bool = False) -> None:
        def __txt_add_command(command: discord.ext.commands.Command, prefix: str) -> str:
            if prefix: prefix += " "
            if not command.hidden:
                return f"**{self.__discord_bot.command_prefix}{prefix}{command.name}:** {command.description}\n\n"
            return ""

        def __iterate_command_list(text: str, command_list_iterator, prefix: str) -> str:
            for command in command_list_iterator():
                command: discord.ext.commands.Command
                if not command.hidden:
                    text += __txt_add_command(command=command, prefix=prefix)
                # Check if command is subcommand
                if isinstance(command, discord.ext.commands.GroupMixin):
                    if prefix:
                        new_prefix = f"{prefix} {command.name}"
                    else:
                        new_prefix = command.name
                    text = __iterate_command_list(text=text, command_list_iterator=command.walk_commands,
                                                  prefix=new_prefix)
            return text

        for _topic, _list_of_commands in help_commands_dictionary.items():
            _list_of_commands.sort()
            command_list = [self.__discord_bot.all_commands[__command_name] for __command_name in _list_of_commands]

            _txt = "‎\n" + __iterate_command_list(text="", prefix="", command_list_iterator=command_list.__iter__)

            if end:
                _txt += "\n"
            else:
                _txt += "‎\n"
            embed.add_field(name=f"‎\n{_topic}", value=_txt, inline=False)

    def _general(self) -> Embed:
        embed = self.__return_embed_template()

        # # Add main commands part 1
        # for _topic, _command_list in _help_commands_part1.items():
        #     # _command_list.sort()
        #     _txt = "‎\n"
        #     for _command in _command_list:
        #         __command = self.__discord_bot.all_commands[_command]
        #         if not __command.hidden:
        #             _txt += f"**{self.__discord_bot.command_prefix}{__command.name}:**         {__command.description}\n\n"
        #     _txt += "‎\n"
        #     embed.add_field(name=f"‎\n{_topic}", value=_txt, inline=False)

        # Add main commands part 1
        self._manage_help_commands_dictionary(help_commands_dictionary=_help_commands_part1, embed=embed)

        # Add account binding commands
        # ## Get commands/subcomands in list
        # _binding_commands = []
        # for _command in self.__discord_bot.all_commands['link'].walk_commands():
        #     _binding_commands.append(_command)
        #     # print(_command)
        # _binding_commands.append(self.__discord_bot.all_commands['unlink'])

        # ## Generate embed text
        # _txt = "‎\n"
        # for _command in _binding_commands:
        #     if not _command.hidden:
        #         _txt += f"**{self.__discord_bot.command_prefix}{_command.name}:**         {_command.description}\n\n"
        # _txt += "‎\n"
        # embed.add_field(name="‎\n:knot: __**Account bindings**__", value=_txt, inline=False)

        # Add list help commands
        for _topic, _command_list in _additional_commands.items():
            _txt = "‎\n"
            for _command, _description in _command_list.items():
                _txt += f"**{self.__discord_bot.command_prefix}{_command}:**         {_description}\n\n"
            _txt += "‎\n"
            embed.add_field(name=f"‎\n{_topic}", value=_txt, inline=False)

        # Add main commands part 2
        self._manage_help_commands_dictionary(help_commands_dictionary=_help_commands_part2, embed=embed, end=True)
        # for _topic, _command_list in _help_commands_part2.items():
        #     _command_list.sort()
        #     # _txt = ""
        #     _txt = "‎\n"
        #     for _command in _command_list:
        #         __command = self.__discord_bot.all_commands[_command]
        #         if not __command.hidden:
        #             _txt += f"**{self.__discord_bot.command_prefix}{__command.name}:**         {__command.description}\n\n"
        #             # _txt += f"‎\n**{self.__discord_bot.command_prefix}{__command.name}:**         {__command.description}>:(\n"
        #     # _txt += "‎\n"
        #     embed.add_field(name=f"‎\n{_topic}", value=_txt, inline=False)

        # # Add Miscellany commands
        # _txt = "‎\n"
        # for _command in _miscellany_commands:
        #     __command = self.__discord_bot.all_commands[_command]
        #     if not __command.hidden:
        #         _txt += f"- **{__command.name}**\n"
        # embed.add_field(name="‎\n:whale: __**Miscellany**__", value=_txt, inline=False)
        # return embed

        #
        # # Add List of available thingies
        # _txt = "‎\n"
        # for _command in _available_app_commands:
        #     __command = self.__discord_bot.all_commands[_command]
        #     if not __command.hidden:
        #         _txt += f"- **{__command.name}**\n"
        # embed.add_field(name="‎\n:bat: Available app/slash commands:", value=_txt, inline=False)
        return embed

    @property
    def profile(self) -> Embed:
        return self._profile()

    def _profile(self) -> Embed:
        embed_list = []
        embed = self.__return_embed_template()
        embed_list.append(embed)
        txt = (f"The **{self.__discord_bot.command_prefix}profile** command returns the Steam account of the user, "
               f"and their current active game (if there is one).\n\nYou can also target another user to display "
               f"their profile.")

        embed.add_field(name="", value=txt)
        # images = ["https://i.imgur.com/aVPfFzR.png"]
        images = ["https://i.imgur.com/bX30fbA.png"]
        for _image_url in images:
            _embed = self.__return_embed_image_template
            _embed.set_image(url=_image_url)
            embed_list.append(_embed)
        return embed_list

    @property
    def usage(self) -> list[Embed]:
        return self._usage()

    def _usage(self) -> list[Embed]:
        embed_list = []
        embed = self.__return_embed_template()
        embed_list.append(embed)
        # 1. Link your Steam account to the Discord bot (doesn't require login nor authentication or anything like that), for more information about this step use the command `{self.__discord_bot.command_prefix}help link`.
        txt = f"""
```md
1. Link your Steam account using your Vanity URL (no password nor authentication used). Use {self.__discord_bot.command_prefix}help link` for more information.

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
        txt = f"If you haven't linked your Steam account use the command **{self.__discord_bot.command_prefix}help link** to get help on that.\n\nOnce you have linked your steam account through you can use commands such **{self.__discord_bot.command_prefix}lobby** or **{self.__discord_bot.command_prefix}shlink** to post a lobby.\n\nYou can select another user to post their lobby."

        embed.add_field(name="", value=txt, inline=False)
        images = ["https://i.imgur.com/VWk90iV.png", "https://i.imgur.com/w5DN6m0.png"]
        # images = ["https://i.imgur.com/BsjU1ps.png", "https://i.imgur.com/0D83hsz.png"]
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
        # /embed_vanity = self.__return_embed_template()
        # embed_steamidthats = self.__return_embed_template()
        # embed_list.append(embed)

        # text = f"""
        #     To get the `vanity URL` from your Steam account, go to your profile page, right click on the background and click **copy URL**.
        #
        #     You should have copied something like this:
        #
        #       steamcommunity.com/id/**SavageBidoof**/
        #
        #     From that URL, the vanity URL is **SavageBidoof**.
        #
        #     Now you just need to use the link command appending the Steam vanity URL:
        #
        #       **{self.__discord_bot.command_prefix}link savagebidoof**
        #
        #     To unlink the account you can use the command **{self.__discord_bot.command_prefix}unlink**
        #     """
        # text = f"""
        #
        #
        #
        #
        #    To unlink the account you can use the command **{self.__discord_bot.command_prefix}unlink**
        #    """
        link_dict = {
            'vanity': {
                'text':f"""
                ‎
                **To link through __Steam ID__ check the __embed from below__**
                
                Go to your profile page, **right click** on the background and click **copy URL**.
                
                If the URL contains **/id/** like this: 
                
                  steamcommunity.com**/id/**SavageBidoof/
                    
                The vanity URL is **SavageBidoof**.
                        
                Now use the following command:
                
                  **{self.__discord_bot.command_prefix}link vanity savagebidoof**
                ‎
                """,
                'image_list': ["https://i.imgur.com/CrVUxbs.png"],
                'title': ":fried_shrimp: Link Steam vanity URL"

            },
            'steamid': {
                'text':f"""
                ‎
                **To link through __Steam vanity URL__ check the __embed from above__**
                
                Go to your profile page, **right click** on the background and click **copy URL**.
                
                If the URL contains **/profile/** like this: 

                  steamcommunity.com**/profile/**76561198170583259/
                
                The SteamID is **76561198170583259**.
                
                Now use the following command:
                
                **{self.__discord_bot.command_prefix}link steamid 76561198170583259**
                ‎
                """,
                'image_list': ['https://i.imgur.com/QxaNM5j.png'],
                'title': ":comet: Link Steam ID"
            }
        }

        _n = 0
        for _topic, _contents in link_dict.items():
            data = HELPER_LINK_SKEL(**_contents)
            text_embed = self.__return_embed_template()
            text_embed.url += str(_n)
            embed_list.append(text_embed)
            text_embed.add_field(name=f'‎\n{data.title}', value=data.text, inline=False)

            for _image_url in data.image_list:
                _image_embed = self.__return_embed_image_template
                _image_embed.url += str(_n)
                _image_embed.set_image(url=_image_url)
                embed_list.append(_image_embed)

            _n += 1

        # text_vanity =

        # text_steamid =

        # embed_vanity.add_field(name="", value=text_vanity, inline=False)
        # embed_steamidthats.add_field(name="", value=text_steamid, inline=False)
        # images = ["https://i.imgur.com/VHdVEj8.png", "https://i.imgur.com/7Ff5rzz.png",
        #           "https://i.imgur.com/KQfOKgt.png"]

        # for _image_url in images:
        #     _embed = self.__return_embed_image_template
        #     _embed.set_image(url=_image_url)
        #     embed_list.append(_embed)

        return embed_list
