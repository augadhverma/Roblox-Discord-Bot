
import random as rnd
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from aiohttp import request


def setup(bot):
    bot.add_cog(Fun(bot))




class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot



    @commands.command(hidden=False,name="dice",aliases=["roll"],usage="`<number>d<number>`\n`number(int)`: A number | Maximum can be 25", description="Rolls the dice")
    @commands.cooldown(1,10, BucketType.user)
    async def roll_dice(self, ctx, die_string):
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 25:
            rolls = [rnd.randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

        else:
            await ctx.send("I can't roll that many dice. Please try a lower number")

    @commands.command(hidden=False,name="echo",description="A simple command that repeats the users input back to them.",usage="`echo [message]`")
    @commands.cooldown(1,3, BucketType.user)
    async def echo(self, ctx, *, message=None):
        message = message or "Please provide something to be repeated."
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(hidden=False,name="choose",aliases=["choice"], description="Chooses between multiple choices. Split choices with a comma (`,`)",usage="`[choices...]`")
    async def choose(self, ctx, *,statement):
        ch = statement.split(",")
        if len(ch) < 2:
            await ctx.send(f"{ctx.author.name} you need to provide minimum of two choices.\n⚠ Note: split them with a comma `,`")

        else:
            await ctx.send(rnd.choice(ch))

    @commands.command(hidden=False,name="slap", aliases=["hit"], description="A command to slap someone", usage="`slap <member> [reason]`")
    @commands.cooldown(1,3, BucketType.user)
    async def slap(self, ctx, member: discord.Member=None,*, reason="for no reason"):
        if member is None:
            await ctx.send(f"<@{self.bot.user.id}> slapped {ctx.author.mention} for not mentioning a user 🤷‍♂️")
        elif member == ctx.author:
            await ctx.send("Why would you slap yourself?")
        elif member is not None:
            member = member
            await ctx.send(f"{ctx.author.mention} slapped {member.mention} {reason}")

