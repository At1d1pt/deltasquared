import discord
from discord.ext import commands

from pretty_help import PrettyHelp

from cogs import fun

from config import TOKEN , PREFIX

bot = commands.Bot(command_prefix=PREFIX, help_command=PrettyHelp(color=discord.Color.from_rgb(35,32,52) , no_category="Help"))
fun.setup(bot)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd , activity=discord.Activity(name=f">help" , type=discord.ActivityType.competing))
    print("Logged in")

bot.run(TOKEN)