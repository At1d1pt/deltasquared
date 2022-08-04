import discord
from discord.ext import commands

import random
import asyncio
import requests

class Fun(commands.Cog):
    '''
    Fun related commands.
    '''
    def __init__(self , bot):
        self.bot = bot

    @commands.command(aliases=["rip"])
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

    @commands.command(aliases=['8ball'])
    async def _8ball(self , ctx , * , question = None):
        '''
        Ask the bot a random 8ball question
        '''
        if question is None:
            await ctx.reply(f"Missing required parameter `question`.\n```\n[p]8ball [question]\n```" , mention_author=False)

        else:
            res_ = [
                'Of course',
                'Maybe',
                'No way',
                'Not sure',
                'Can\'t answer right now',
                'No',
                'I don\'t think so',
                'Yes'
            ]

            await ctx.reply(random.choice(res_) , mention_author=False)

    @commands.command(aliases=["love"])
    async def ship(self , ctx , * , user: discord.User = None):
        '''
        Check your love with someone
        '''
        if user is None:
            await ctx.reply(f"Missing required parameter `user`.\n```\n[p]ship [user]\n```" , mention_author=False)
        else:
            l = random.randrange(0 , 101)
            em = discord.Embed(description=f":heart: {ctx.author.mention} x {user.mention} :heart: **__{l}__**%" , color=discord.Color.from_rgb(255,105,180))

            await ctx.send(embed=em)

    @commands.command()
    async def trivia(self , ctx):
        r = requests.get('https://opentdb.com/api.php?amount=1&category=17&difficulty=easy&type=multiple').json()
        opt: list = r['results'][0]['incorrect_answers']
        opt.append(r['results'][0]['correct_answer'])
        random.shuffle(opt)

        options = {
            'a': opt[0],
            'b': opt[1],
            'c': opt[2],
            'd': opt[3]
        }

        s = f'''
A: {opt[0]}
B: {opt[1]}
C: {opt[2]}
D: {opt[3]}
        '''
        em = discord.Embed(title=r['results'][0]['question'] , description=s , color=discord.Color.green()).set_author(name=ctx.author.name , icon_url=str(ctx.author.avatar_url)).add_field(name="Category" , value=r['results'][0]['category'])
        await ctx.send(content='' , embed=em)
        del s

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            m = await self.bot.wait_for('message' , check=check , timeout=20)
            if options[m.content.lower()] == r['results'][0]['correct_answer']:
                await m.reply(embed=discord.Embed(description="Correct Answer!" , color=discord.Color.green()))
            else:
                await m.reply(f"Wrong answer!\nCorrect Option: [{r['results'][0]['correct_answer']}]")
        except TimeoutError:
            await ctx.send("Timed Out")

