import discord
from discord.ext import commands
from datetime import datetime

def setup(bot):
    bot.add_cog(Help(bot))



class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    def get_commands(self):
        helptext = []
        for command in self.bot.commands:
            if command.hidden == True:
                pass
            else:
                helptext.append(command)
        
        embed = discord.Embed(colour=self.bot.defaultcolour, title="Help", description="All the commands")
        embed.add_field(name="Support",value="For more help, join the official bot support server: https://discord.gg/CTuUKJJ",inline=False)
        embed.add_field(name="Commands",value=", ".join([command.name for command in helptext]),inline=False)


        return embed

    @commands.command(name="help", description="Shows all the bot's command", aliases=["h","commands"],usage="`[command]`")
    async def help_command(self, ctx, cmd = None):
        

        if cmd is None:
            base_embed = self.get_commands()
            await ctx.send(embed=base_embed)

        elif cmd != None:
            command = self.bot.get_command(cmd)
            if command:
                aliases = []
                for alias in command.aliases:
                    aliases.append(alias)

                command.description = command.description or "No description provided."
                embed = discord.Embed(colour=self.bot.defaultcolour,title="Help",description=f"`{command.name}`: {command.description}", timestamp=datetime.utcnow())
                embed.add_field(name="Aliases",value=" ,".join(aliases) if len(aliases) >= 1 else "No aliases",inline=False)
                embed.add_field(name="Usage", value=command.usage if command.usage != None else f"`{command.name}`", inline=False)
                embed.set_footer(text="<> - Required | [] - Optional")

                await ctx.send(embed=embed)

            else:
                inv_embed = self.get_commands()
                await ctx.send("Invalid Command Usage. Activiating Help...")
                await ctx.send(embed=inv_embed)