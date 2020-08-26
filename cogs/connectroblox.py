import robloxapi
import discord
from discord.ext import commands
from datetime import datetime
import requests

from discord.ext.commands import BucketType

def setup(bot):
    bot.add_cog(Roblox(bot))



class Roblox(commands.Cog):
        def __init__(self,bot):
            self.bot = bot

        @commands.command(hidden=False,name="verify", description="Command to link Roblox Account to Discord Account")
        async def verify(self, ctx):
            embed=discord.Embed(title="Verify", description="To verify yourself, [click here](https://verify.eryn.io/)", timestamp=datetime.utcnow())
            await ctx.send(embed=embed)


        @commands.command(hidden=False,name="account-info",aliases=["accountinfo","ai"],description="Shows the information of the user's Roblox Account", usage="`[member]`")
        @commands.cooldown(1,5, BucketType.user)
        async def rbx(self, ctx, member:discord.Member = None):
            try:
                member = member or ctx.author
            
                response = requests.get(f"https://verify.eryn.io/api/user/{member.id}")
                name = response.json()

                if name["status"] == "ok":
                    user = await self.bot.robloxclient.get_user_by_id(name['robloxId'])
                    av = await user.get_detailed_user()

                    gamepasses = await user.get_gamepasses()


                    embed = discord.Embed(colour=self.bot.defaultcolour,title=f"Roblox Information about {member.name}",timestamp=datetime.utcnow())
                    embed.set_footer(text=ctx.author.name)
                    embed.set_thumbnail(url=av.avatar_url)

                    fields=[("Username",name['robloxUsername']),
                            ("Roblox Id",name['robloxId']),
                            ("Discord Id",member.id),

                            ("Blurb",av.blurb),
                            ("Gamepasses",f"{len(gamepasses)} owned"),
                            ("Different Account?",f"Chane your acount [here](https://verify.eryn.io)")]

                    for name, value in fields:
                        embed.add_field(name=name, value=value, inline=False)

                    await ctx.send(embed=embed)

                elif name['status'] == "error":
                    embed = discord.Embed(title=f"{member.name} is not verified",
                                        colour=0xff0000,
                                        timestamp=datetime.utcnow(),
                                        description="[Click here](https://verify.eryn.io) to verify")
                    embed.set_footer(text=ctx.author.name)

                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(e)

        @commands.command(hidden=False,name="setrank", description="Sets rank of a user to mentioned group rank", usage="`setrank <RobloxName> <Rank>`\n\nThe rank name should be same as in thr robloxgroup")
        @commands.is_owner()
        @commands.cooldown(1,5, BucketType.guild)
        async def setrank(self, ctx, name, *, rank):
            group = await self.bot.robloxclient.get_group(self.bot.maingroup)
            user = await self.bot.robloxclient.get_user_by_username(name)
            roles = await group.get_group_roles()
            role = list(filter(lambda x: x.name.lower() == rank.lower(), roles))


            if len(role) == 0:
                embed=discord.Embed(description=f"Role `{rank}` was not found\nPlease use the exact rank from the group.\nIf you think this was an error, please contact the [support server](https://discord.gg/MjZ574g)",colour=0xff0000)
                await ctx.send(embed=embed)
            try:
                request = await group.set_rank(user.id, role[0].id)
                if request == 200:
                    embed = discord.Embed(description=f"{name} was succesfully ranked `{role[0].name}`", colour=0x00ff00)
                    await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(e, delete_after=10)

        @commands.command(hidden=False,name="gamepasses",aliases=["all-gamepasses","allgamepass"],description="Shows all the user's gamepasses",usage="`gamepasses [member]`")
        @commands.cooldown(1,5, BucketType.guild)
        async def gamepasses(self, ctx, member:discord.Member = None):
            member = member or ctx.author

            response = requests.get(f"https://verify.eryn.io/api/user/{member.id}")
            name = response.json()

            if name['status'] == "ok":
                user = await self.bot.robloxclient.get_user_by_id(name["robloxId"])
                gamepasses = await user.get_gamepasses()
                embed=discord.Embed(title="All Gamepasses", colour=self.bot.defaultcolour,timestamp = datetime.utcnow(),
                                    description=", ".join([gamepass.name for gamepass in gamepasses]))

                embed.add_field(name="Different Account?",value=f"Chane your acount [here](https://verify.eryn.io)")
                embed.set_footer(text=f"Username: {name['robloxUsername']} | ID: {name['robloxId']}")

                await ctx.send(embed=embed)

            elif name['status'] == "error":
                embed = discord.Embed(colour=0xff0000, 
                                    title=f"{member.name} is not verified",
                                    timestamp=datetime.utcnow(),
                                    description="[Verify here](https://verify.eryn.io)")

                await ctx.send(embed=embed)

        @commands.command(hidden=False,name="groupinfo",description="Gets the groupinfo of the main group",aliases=["gi"])
        @commands.cooldown(1,10,BucketType.guild)
        async def groupinfo(self, ctx):
            client = self.bot.robloxclient
            group = await client.get_group(self.bot.maingroup)

            roles = await group.get_group_roles()


            embed=discord.Embed(title="Group Info",colour=self.bot.defaultcolour,description=f"[Link to Group](https://www.roblox.com/groups/{group.id})",timestamp=datetime.utcnow())
            fields = [("Group Name",f"`{group.name}`"),
                      ("Group Id", group.id),
                      ("Group Member", group.member_count),
                      ("Owner",group.owner.name),
                      ("Roles ", len(roles)),
                      ("Current Shout", group.shout['body'])]

            for name, value in fields:
                embed.add_field(name=name,value=value,inline=False)


            await ctx.send(embed=embed)


        @commands.command(hidden=False,name="shout",description="Posts a shout",usage="`shout <message>`\n\n⚠ The Roblox User should have the following permissions: `Post on group wall`")
        @commands.is_owner()
        @commands.cooldown(1,5,BucketType.guild)
        async def shout(self, ctx, *,mesage:str):
            client = self.bot.robloxclient
            group = await client.get_group(self.bot.maingroup)

            try:

                await group.post_shout(mesage)
                embed = discord.Embed(colour=0x00ff00,title="Post Successful",description=f"Shout: {mesage}",timestamp=datetime.utcnow())
                embed.set_footer(text="Was made on")
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(e)

        @commands.command(hidden=False,name="roblox-info",aliases=["robloxinfo","ri"],description="Shows the member's info in the maingroup", usage="`roblox-info [member]`")
        @commands.cooldown(1,5,BucketType.user)
        async def memrbx(self, ctx, member:discord.Member = None):
            try:
                member = member or ctx.author
            
                response = requests.get(f"https://verify.eryn.io/api/user/{member.id}")
                name = response.json()

                if name["status"] == "ok":
                    user = await self.bot.robloxclient.get_user_by_id(name['robloxId'])
                    av = await user.get_detailed_user()

                    role = await user.get_role_in_group(self.bot.maingroup)

                    embed = discord.Embed(colour=self.bot.defaultcolour,title=f"Group Information on {member.name}",timestamp=datetime.utcnow(),description="Change account [here](https://verify.eryn.io)")
                    embed.set_footer(text=f"Roblox ID: {name['robloxId']}")
                    embed.set_thumbnail(url=av.avatar_url)

                    fields=[("Username",name['robloxUsername'], False),
                            ("Role",role.name, True),
                            (f"Users in {role.name}",role.member_count,True),
                            (f"Rank of {role.name}",role.rank, True)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await ctx.send(embed=embed)

                elif name['status'] == "error":
                    embed = discord.Embed(title=f"{member.name} is not verified",
                                        colour=0xff0000,
                                        timestamp=datetime.utcnow(),
                                        description="[Click here](https://verify.eryn.io) to verify")
                    embed.set_footer(text=ctx.author.name)

                    await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(e)

        @commands.command(hidden=False,name="exile",aliases=["kick"],description="Exiles the user from the maingroup",usage="`exile <RobloxUsername>`")
        @commands.is_owner()
        @commands.cooldown(1,5,BucketType.user)
        async def exilefromgroup(self, ctx, member):
            try:
                client = self.bot.robloxclient
                group = await client.get_group(self.bot.maingroup)

                user = await self.bot.robloxclient.get_user_by_username(member)

                await group.exile(user.id)
                embed = discord.Embed(colour=0x00ff00, title=f"{member} was successfully exiled from the group!", timestamp=datetime.utcnow())
                embed.set_footer(text=ctx.author.name)

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(e)