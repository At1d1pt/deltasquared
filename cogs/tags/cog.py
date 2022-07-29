import discord
from discord.ext import commands

import json
import time

class Tags(commands.Cog):
    '''
    Simple tags.
    '''
    def __init__(self , bot):
        self.bot = bot

    async def get_tags(self):
        with open("cogs\\tags\\data.json" , "r") as f:
            tags = json.load(f)

        return tags

    async def new_tag(self , name: str , response: str , creator: discord.User , modify: bool = False):
        tags = await self.get_tags()
        if name in tags:
            if modify:
                tags[name] = {}
                tags[name]['response'] = response
                tags[name]['creator'] = creator.id

                with open("cogs\\tags\\data.json" , "w") as f:
                    json.dump(tags , f)

            else:
                return 1
        else:
            tags[name] = {}
            tags[name]['response'] = response
            tags[name]['creator'] = creator.id

            with open("cogs\\tags\\data.json" , "w") as f:
                json.dump(tags , f)

    @commands.command()
    async def tag(self , ctx , tag_ = None):
        '''
        Use a tag
        '''

        variable_tags = {
            '<user.mention>': ctx.author.mention,
            '<user.name>': ctx.author.name,
            '<user.tag>': str(ctx.author.discriminator),
            '<user.avatar_url>': str(ctx.author.avatar_url),
            '<time>': f'<t:{round(time.time())}:F>',
            '@everyone': 'Everyone',
            '@here': 'Online Users',
            '<guild.members>': str(ctx.channel.guild.member_count),
            '<guild.name>': ctx.channel.guild.name,
            '<channel.name>': ctx.channel.name,
            '<channel.mention>': f'<#{ctx.channel.id}>'
        }

        if tag_ is None:
            await ctx.reply(":x: Missing required parameter `tag`.\n```\n[p]tag [tag]\n```" , mention_author = False)
        
        else:
            key = tag_.lower()
            tags = await self.get_tags()
            if key not in tags:
                await ctx.reply(":x: Tag '{}' not found.".format(key) , mention_author=False)
            else:
                response = tags[key]['response']

                for x in variable_tags:
                    response = response.replace(x , variable_tags[x])

                await ctx.reply(response , mention_author = False)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def create_tag(self , ctx , name=None , * , response=None):
        '''
        Create a new tag
        '''
        if name is None or response is None:
            await ctx.reply(":x: Missing required parameter `name` or `response`.\n```\n[p]create_tag [name] [response]\n```" , mention_author=False)

        else:
            res = await self.new_tag(name=name.lower() ,response=response, creator=ctx.author)

            if res == 1:
                await ctx.send(":x: Tag with name `{}` already exists.".format(name))
            else:
                await ctx.send("Successfully created a new tag.")
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def modify_tag(self , ctx , name=None , * , response=None):
        '''
        Modify an existing tag
        '''
        if name is None or response is None:
            await ctx.reply(":x: Missing required parameter `name` or `response`.\n```\n[p]modify_tag [name] [response]\n```" , mention_author=False)
        else:
            await self.new_tag(name.lower() , response , ctx.author , modify=True)
            await ctx.send("Successfully modified `{}`".format(name))

    @commands.command()
    async def tags(self , ctx):
        '''
        Get a list of available tags
        '''

        tags = await self.get_tags()
        em = discord.Embed(title="Available Tags" , color=discord.Color.blurple()).set_author(name=ctx.author.name , icon_url=str(ctx.author.avatar_url))

        for tag in tags:
            creator = await self.bot.fetch_user(tags[tag]["creator"])
            em.add_field(name=tag , value=f'Created by: {creator.mention}' , inline=False)

        await ctx.send(embed=em)
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete_tag(self , ctx , name=None):
        '''
        Delete a tag
        '''
        if name is None:
            await ctx.reply(":x: Missing required parameter `name`.\n```\n[p]delete_tag [name]\n```" , mention_author = False)
        else:
            tags = await self.get_tags()

            try:
                del tags[name]

                with open("cogs\\tags\\data.json" , "w") as f:
                    json.dump(tags , f)

                await ctx.send("Deleted tag `{}`".format(name))

            except:
                await ctx.send(f":x: Tag with name `{name}` does not exist.")

    @create_tag.error
    async def create_tag_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(":x: You must have `manage_messages` permission to run this command.")
        else:
            print(error)

    @delete_tag.error
    async def delete_tag_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(":x: You must have `manage_messages` permission to run this command.")

    @modify_tag.error
    async def modify_tag_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(":x: You must have `manage_messages` permission to run this command.")