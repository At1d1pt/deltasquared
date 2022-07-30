import discord
from discord.ext import commands

import json
import time

class AutoResponse(commands.Cog):
    def __init__(self , bot):
        self.bot = bot

    async def get_autoresponses(self):
        with open("cogs\\autoresponse\\data.json" , "r") as f:
            ar = json.load(f)

        return ar

    async def new_autoresponse(self , name: str , response: str , creator: discord.User , modify: bool = False):
        ars = await self.get_autoresponses()
        if name in ars:
            if modify:
                ars[name] = {}
                ars[name]['response'] = response
                ars[name]['creator'] = creator.id

                with open("cogs\\autoresponse\\data.json" , "w") as f:
                    json.dump(ars , f)

            else:
                return 1
        else:
            ars[name] = {}
            ars[name]['response'] = response
            ars[name]['creator'] = creator.id

            with open("cogs\\autoresponse\\data.json" , "w") as f:
                json.dump(ars , f)

    @commands.command()
    @commands.has_permissions()
    async def create_ar(self , ctx , trigger: str = None , * , response: str = None):
        '''
        Create a new auto-response
        '''

        if trigger is None or response is None:
            await ctx.reply("Missing required parameter `trigger` or `response`.\n```\n[p]create_ar [trigger] [response]\n```")
        else:
            res = await self.new_autoresponse(name=trigger.lower() , response=response , creator=ctx.author , modify=True)

            await ctx.send(f"Autoresponse `{trigger}` created.")

    @commands.command()
    async def ars(self , ctx):
        '''
        Get a list of available autoresponses
        '''

        s = await self.get_autoresponses()
        em = discord.Embed(title="Available Autoresponses" , color=discord.Color.blurple()).set_author(name=ctx.author.name , icon_url=str(ctx.author.avatar_url))

        for ar in s:
            creator = await self.bot.fetch_user(s[ar]["creator"])
            em.add_field(name=ar , value=f'Created by: {creator.mention}' , inline=False)

        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self , msg: discord.Message):
        if msg.author.id == self.bot.user.id:
            return
        else:
            s = await self.get_autoresponses()
            
            variable_tags = {
            '<user.mention>': msg.author.mention,
            '<user.name>': msg.author.name,
            '<user.tag>': str(msg.author.discriminator),
            '<user.avatar_url>': str(msg.author.avatar_url),
            '<time>': f'<t:{round(time.time())}:F>',
            '@everyone': 'Everyone',
            '@here': 'Online Users',
            '<guild.members>': str(msg.channel.guild.member_count),
            '<guild.name>': msg.channel.guild.name,
            '<channel.name>': msg.channel.name,
            '<channel.mention>': f'<#{msg.channel.id}>'
            }

            for ar in s:
                if ar in msg.content.lower():
                    response = s[ar]['response']

                    for x in variable_tags:
                        response = response.replace(x , variable_tags[x])
                    
                    await msg.reply(response , mention_author=False)
                    break