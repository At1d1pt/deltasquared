import discord
from discord.ext import commands

from pretty_help import PrettyHelp

from cogs import fun , moderation , tags

from config import TOKEN , PREFIX

bot = commands.Bot(command_prefix=PREFIX, help_command=PrettyHelp(color=discord.Color.from_rgb(35,32,52) , no_category="Help"))
cogs = [fun , moderation , tags]

for cog in cogs:
    cog.setup(bot)
    print('Loaded '+cog.__name__)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd , activity=discord.Activity(name=f">help" , type=discord.ActivityType.competing))
    print("Logged in")

bot.run(TOKEN)