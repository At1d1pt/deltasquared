import discord
from discord.ext import commands

import random
import asyncio

class Fun(commands.Cog):
    '''
    Fun related commands.
    '''
    def __init__(self , bot):
        self.bot = bot

    @commands.command()
    async def respect(self , ctx: commands.Context , user: discord.Member = None):
        '''
        Pay your respects for someone.
        '''
        if user is None:
            await ctx.send(":x: Missing required parameters.\n```\n[p]respect [user]\n```")
        
        else:
            emoji = '<:respect:883616663239524382>'
            m: discord.Message = await ctx.send(f"Pay your respect for **{user}** by reacting with {emoji}.")
            await m.add_reaction(emoji)
            await asyncio.sleep(5)
            nm = await ctx.channel.fetch_message(m.id)
            await m.reply(f"__{len(nm.reactions)}__ user(s) paid their respect for **{user}**." , mention_author=False)
            await asyncio.sleep(0.5)
            await m.clear_reactions()