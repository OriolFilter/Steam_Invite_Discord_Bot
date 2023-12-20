# This doc is used for the help command on the discord bot.

txt_help_help = """
```md
### Bot commands commands
lobby           Returns the lobby of the user. A discord user can be mentioned to return their lobby. If the short link (shlink) functionality is enabled on the bot, the lobby link will be linked to a link shortener service and allow the users to click on the Steam link.
profile         Returns the profile of the user and their active game. A discord user can be mentioned to return their profile.
shlink          Behaves like the `lobby` command, but instead of  

### Account bindings
link            Sets up your account providing the vanity url. If you need help setting it up use the command `help link`.
unlink          Use this to unlink the account and will delete the database entry.

### Admin commands
sync            Sync the commands with all the servers (Bot Owner only)

### Help commands
help            Returns this list. This also has an alias `help general`
help link       How to link your Steam account with this bot.
help lobby      How to use the lobby command (and shlink)
help usage      Example on how to use this bot/Commands and stuff (sort of functionalities)

### Miscellany 
botinvite       Returns a link to invite this bot to your server. 
version         Prints the current version

### Available Slash/App commands
- help
- link
- lobby
- profile
- shlink
- unlink
```
> Note: To use Slash/Apps commands type `/` on the chat and proceed to select the desired command. 
"""

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
TODO
"""

txt_help_profile = """
TODO
"""

HELP_DIC = {
    'general': txt_help_help,
    'link': txt_help_link,
    'lobby': txt_help_lobby,
    'profile': txt_help_profile,
    'usage': txt_help_usage,
}
