import discord
from discord import app_commands
import os

from discord.ext import commands

prefix = "?"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)
tree = bot.tree

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("synced")

@bot.command()
async def ping(ctx):
    '''
    This text will be shown in the help command
    '''

    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(latency)


@app_commands.command()
@app_commands.allowed_installs(guilds=False, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def useable_only_users(interaction: discord.Interaction):
    await interaction.response.send_message("I am only installed to users, but can be used anywhere.")






# bot = discord.Client(intents=discord.Intents.none())


# @bot.command()
@tree.command()
# @app_commands.allowed_installs(guilds=False, users=True) # users only, no guilds for install
# @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # all allowed
async def hello(interaction: discord.Interaction) -> None:
    # await interaction.send("test")
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")




bot.run(os.getenv("DISCORD_TOKEN"))  # Where 'TOKEN' is your bot token
