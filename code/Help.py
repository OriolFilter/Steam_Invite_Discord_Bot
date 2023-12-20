# This doc is used for the help command on the discord bot.

txt_help_help = """
```md
### Bot commands commands
link            Sets up your account providing the vanity url
lobby           If no user is specified, posts the caller lobby in the chat, if...
profile         Returns Steam account from the user and their current open game...
shlink          Stands for "short link"
unlink          Use this to unlink the account.

### Admin commands
sync            Sync the commands with all the servers (Bot Owner only)

### Help commands
help            Returns a list of available commands.
help link       How to link your Steam account with this bot.
help usage      Example on how to use this bot  (move to help usage)

### Miscellany 
bot_invite      In case someone wants to add this bot to their server use the li...
version         Prints the current version and the Build Date

### Available Slash/App commands
- profile (not added yet)
- lobby (not added yet)
- shlink (not added yet)
- help
```
"""

# sync_server     Sync the commands the current server (Admin permissions required to that specific server)
# howto           Example on how to use this bot  (move to help usage)
# vanity          How to use the link command, and from where to extract the vanit...

txt_help_link = """


https://i.imgur.com/VHdVEj8.png
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

HELP_DIC = {
    'general': txt_help_help,
    'link': txt_help_link,
    'usage': txt_help_usage,
    'lobby': txt_help_lobby
}
