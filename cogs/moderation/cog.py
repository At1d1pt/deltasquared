import json
import asyncio

import discord
from discord.ext import commands

from config import LOG_CHANNEL

async def log(bot: commands.Bot , embed: discord.Embed):
    channel = bot.get_channel(LOG_CHANNEL)
    await channel.send(embed=embed)

class Moderation(commands.Cog):
    '''
    Moderation related commands.
    '''

    def __init__(self , bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self , msg: discord.Message):
        if msg.guild is None or msg.author.id == self.bot.user.id:
            return
        else:
            with open("cogs\\moderation\\data.json" , "r") as f:
                blacklist_ = json.load(f)['blacklist']

            for x in blacklist_:
                if x in msg.content.lower():
                    await msg.delete()
                    await msg.channel.send(f"{msg.author.mention}, your message contains blacklisted words.")
                    em = discord.Embed(title="Blacklisted Message" , description=f"Message containing the blacklisted word '{x}' was deleted in <#{msg.channel.id}>." , color=discord.Color.red()).add_field(name="Content" , value=msg.clean_content , inline=False).set_footer(text=f"{msg.author}")
                    await log(self.bot , em)
                    break
                else:
                    continue

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def blacklist(self , ctx , * , content: str = None):
        '''
        Blacklist a word.
        '''
        if content is None:
            await ctx.send(f":x: Missing required parameter `content`.\n```\n[p]blacklist [content]\n```")
        else:
            with open("cogs\\moderation\\data.json" , "r") as f:
                raw = json.load(f)

            if content in raw['blacklist']:
                await ctx.send(f"||{content}|| is already blacklisted." , delete_after=2)
            else:
                raw['blacklist'].append(content)
                with open("cogs\\moderation\\data.json" , "w") as fp:
                    json.dump(raw , fp)

                em = discord.Embed(title="Message Blacklisted" , description=f"{ctx.author.mention} blacklisted '{content}'." , color=discord.Color.red())
                await log(self.bot , em)
                await ctx.send(f"Blacklisted ||{content}||.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def whitelist(self , ctx , * , content: str = None):
        '''
        Whitelist a word.
        '''
        if content is None:
            await ctx.send(f":x: Missing required parameter `content`.\n```\n[p]whitelist [content]\n```")
        else:
            with open("cogs\\moderation\\data.json" , "r") as f:
                raw = json.load(f)

            try:
                raw['blacklist'].remove(content)
                em = discord.Embed(title="Message Whitelisted" , description=f"{ctx.author.mention} whitelisted '{content}'" , color=discord.Color.green())
                await log(self.bot , em)
                await ctx.send(f"Whitelisted ||{content}||.")
            except:
                await ctx.send(f"||{content}|| is not blacklisted.")

    @blacklist.error
    async def blacklist_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(":x: You must have `manage_messages` permission to run this command.")

    @whitelist.error
    async def whitelist_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(":x: You must have `manage_messages` permission to run this command.")