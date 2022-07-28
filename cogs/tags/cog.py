import discord
from discord.ext import commands

import json

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

    async def new_tag(self , name: str , response: str , creator: discord.User):
        tags = await self.get_tags()
        if name in tags:
            return 1
        else:
            tags[name] = {}
            tags[name]['response'] = response
            tags[name]['creator'] = creator.id

            with open("cogs\\tags\\data.json" , "w") as f:
                json.dump(tags , f)

    @commands.command()
    async def tag(self , ctx , key = None):
        '''
        Use a tag
        '''
        if key is None:
            await ctx.reply(":x: Missing required parameter `key`.\n```\n[p]tag [key]\n```" , mention_author = False)
        
        else:
            key = key.lower()
            tags = await self.get_tags()
            if key not in tags:
                await ctx.reply(":x: Tag '{}' not found.".format(key) , mention_author=False)
            else:
                response = tags[key]['response']
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
            res = await self.new_tag(name=name ,response=response, creator=ctx.author)

            if res == 1:
                await ctx.send(":x: Tag with name `{}` already exists.".format(name))
            else:
                await ctx.send("Successfully created a new tag.")

    @create_tag.error
    async def create_tag_error(self , ctx , error):
        if isinstance(error , commands.MissingPermissions):
            await ctx.send(":x: You must have `manage_messages` permission to run this command.")
        else:
            print(error)