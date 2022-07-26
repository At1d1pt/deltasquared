import discord
from discord.ext import commands

import random

class Fun(commands.Cog):
    '''
    Fun related commands.
    '''
    def __init__(self , bot):
        self.bot = bot

    @commands.command()
    async def respect(self , ctx , user: discord.Member = None):
        if user is None:
            await ctx.send(":x: Missing required parameters.\n```\n[p]respect [user]\n```")
        
        emoji = '<:respect:883616663239524382>'
