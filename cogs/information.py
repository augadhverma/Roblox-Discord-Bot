import discord
from discord.ext import commands
from datetime import datetime, timedelta
from time import time
import platform
import robloxapi
import requests


from discord.ext.commands import BucketType

def setup(bot):
    bot.add_cog(Information(bot))




class Information(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def botut(self):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        ut = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        return ut

    @commands.command(name="userinfo",aliases=["ui","whois","uinfo"],description="Show a user's information", usage='`userinfo [member]`')
    async def user_info(self, ctx, member:discord.Member=None):
        member = member or ctx.author
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=self.bot.defaultcolour, description=f"Some useful information about {member.name}",timestamp=datetime.utcnow()) 
        #Shows the user's highest roles' colour. For a custom colour replace member.colour with 0xhexcode; an example will be: colour=0xffff00
        embed.set_author(name=member)
        embed.set_footer(text=f"USER ID: {member.id}")
        embed.set_thumbnail(url=member.avatar_url)

        fields = [("Created",member.created_at.strftime("%d-%m-%Y %H:%M")),
                  ("Joined",member.joined_at.strftime("%d-%m-%Y %H:%M")),
                  ("Roles", " ,".join([role.mention for role in roles]))]

        for name, value in fields:
            embed.add_field(name=name,value=value,inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="serverinfo",aliases=["si","sinfo"],description="serverinfo Shows the server's information")
    async def server_info(self, ctx):
        try:
            x = datetime.now()
            a= x.strftime("%x")

            embed = discord.Embed(title=ctx.guild.name, colour=self.bot.defaultcolour, description=f"Some useful information about {ctx.guild.name}",timestamp=datetime.utcnow())
            #Shows the user's highest roles' colour. For a custom colour replace member.colour with 0xhexcode; an example will be: colour=0xffff00

            statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "streaming", ctx.guild.members)))]

            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=ctx.author.name)
            fields = [("ID",ctx.guild.id),
                      ("Owner", ctx.guild.owner),
                      ("Created", a),
                      ("Channels", f"Text: {len(ctx.guild.text_channels)}\nVoice: {len(ctx.guild.voice_channels)}"),
                      ("Members", f"\\🟢 {statuses[0]} \\🟡 {statuses[1]} \\🔴 {statuses[2]} \\⚪ {statuses[3]} \\🟣 {statuses[4]}\nTotal: {len(ctx.guild.members)}"),
                      ("Roles", len(ctx.guild.roles)),
                      ("Server Region",ctx.guild.region)]


            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(e)

    @commands.command(name="ping",description="Shows the ping")
    async def botping(self, ctx):
        start = time()

        embed = discord.Embed(colour=self.bot.defaultcolour,description="Pinging...")
        message = await ctx.send(embed=embed)
        end = time()

        rbxstart = time()
        
        await self.bot.robloxclient.get_user_by_id(611401554)
        
        rbxend = time()

        newEmbed = discord.Embed(colour=self.bot.defaultcolour, title="Pong! 🏓",timestamp=datetime.utcnow(),
                                description=f"""DWSP latency: {self.bot.latency*1000:,.0f} ms.
    Response time: {(end-start)*1000:,.0f} ms.
    RobloxApi response time: {(rbxend-rbxstart)*1000:,.0f} ms. """)
        newEmbed.set_footer(text=ctx.author.name)

        await message.edit(embed=newEmbed)

    @commands.command(name="invite", description="Invite the bot to your other server with this command")
    async def botinvite(self, ctx):
        embed=discord.Embed(timestamp=datetime.utcnow(),colour=self.bot.defaultcolour,title="Invite",description=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot")
        embed.add_field(name="Source", value="https://github.com/ItsArtemiz/Roblox-Discord-Bot")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)

    @commands.command(name="botinfo",description="Some useful information about the bot", aliases=["stats"])
    async def botinformation(self, ctx):
        start = time()

        embed = discord.Embed(colour=self.bot.defaultcolour,description="Retreiving useful information...")
        message = await ctx.send(embed=embed)
        end = time()

        rbxstart = time()
        
        await self.bot.robloxclient.get_user_by_id(611401554)
        
        rbxend = time()

        newEmbed = discord.Embed(colour=self.bot.defaultcolour,title="Bot Info",timestamp=datetime.utcnow())
        newEmbed.set_footer(text=ctx.author.name)

        fields=[("Bot Developer","ItsArtemiz#8858"),
                ("Source","https://github.com/ItsArtemiz/Roblox-Discord-Bot"),
                ("Bot Version",self.bot.version),
                ("Uptime",self.botut()),
                ("Language","Python"),
                ("Python Version",platform.python_version()),
                ("discord.py Version", discord.__version__),
                ("DWSP latency",f"{self.bot.latency*1000:,.0f} ms."),
                ("Response Time", f"{(end-start)*1000:,.0f} ms"),
                ("RobloxApi Response Time",f"{(rbxend-rbxstart)*1000:,.0f} ms.")]

        for name, value in fields:
            newEmbed.add_field(name=name, value=value)

        await message.edit(embed = newEmbed)

    @commands.command(name="uptime",description="Shows bot's uptime", aliases=["ut"])
    async def botuptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        await ctx.send(f"Uptime: **{days}d, {hours}h, {minutes}m, {seconds}s**")

    @commands.command(name="source",description="Bot's Github Source", timestamp=datetime.utcnow())
    async def botsource(self, ctx):
        embed=discord.Embed(colour=self.bot.defaultcolour,title="Source",timestamp=datetime.utcnow(),description="https://github.com/ItsArtemiz/Roblox-Discord-Bot")
        embed.set_footer(text="ItsArtemiz")

        await ctx.send(embed=embed)

    @commands.command(name="avatar",aliases=["av"],description="Shows the avatar of a user", usage="`avatar [member]`")
    async def av_member(self,ctx, member:discord.Member = None):
        member = member or ctx.author
        ava = member.avatar_url_as(static_format='png')
        embed = discord.Embed(colour=self.bot.defaultcolour,title="Avatar")
        embed.set_image(url=member.avatar_url)
        embed.set_author(name=member, icon_url=member.avatar_url, url=ava)
        await ctx.send(embed=embed)

    @commands.command(name="membercount",aliases=["mc"],description="Shows the membercount of the server")
    async def member_count(self, ctx):
        embed =discord.Embed(colour=self.bot.defaultcolour, timestamp=datetime.utcnow(),title="Member Count",
                             description=f"Total: {len(ctx.guild.members)}\nHumans: {len([Member for Member in ctx.guild.members if not Member.bot])}\nBots: {len([Member for Member in ctx.guild.members if Member.bot])}")
        
        embed.set_footer(text=ctx.author.name)

        await ctx.send(embed=embed)

        