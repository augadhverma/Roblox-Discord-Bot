import discord
from discord.ext import commands
import os
from datetime import datetime

from discord.errors import HTTPException, Forbidden
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown, NotOwner, MissingPermissions)
import robloxapi

defaultprefix = ';' #change the prefix to whatever you want
defaultcolour = 0xcdcdcd #change to the hex code of your liking

client= robloxapi.Client("Your Roblox Cookie")
#Change to your roblox client cookie

owner=[371019056419045376,449897807936225290] # Add discord ids of user who will have owner control over the bot, i.e, can use commands like setrank or shout
maingroup = 0000000

TOKEN = "Your Bot Token"

#Don't share your token with anyone. Tokens are like a password to the bot. If someone has your token, they have full control over your bot.
#If you have accidently revelead it, you can Regenerate it from the application page




#---------------------------------------------------⚠---------------------------------------------------------------------------#





#----- ⚠ DONT CHANGE ANYTHING OR THE BOT WILL MOST LIKELY NOT WORK
intents = discord.Intents.all()
bot = commands.Bot(command_prefix= commands.when_mentioned_or(defaultprefix), case_insensitive=True, owner_ids=owner, intents=intents)
bot.remove_command('help')

bot.launch_time = datetime.utcnow()

bot.defaultprefix = defaultprefix
bot.defaultcolour = defaultcolour
bot.version = "1.0"
bot.robloxclient = client
bot.maingroup = maingroup

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ItsArtemiz#8858"))
    print("Logged in!")


#---- COMMAND ERROR HANDLER --- ⚠ DON'T CHANGE ANYTHING OR YOU WILL MOST PROBABLY RECIEVE WARNINGS
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("One or more required arguments are missing.")

        
    elif isinstance(error, CommandNotFound):
        pass

    elif isinstance(error, BadArgument):
        await ctx.send(error)

    elif isinstance(error, CommandOnCooldown):
        await ctx.send(f"That command is on {str(error.cooldown.type).split('.')[-1]} cooldown. Try again in {error.retry_after:,.2f} secs.")

    
    elif isinstance(error, NotOwner):
        await ctx.send("You don't have enough permissions to run that command")

    elif isinstance(error, MissingPermissions):
        await ctx.send("You don't have enough permissions to run that command")

    elif hasattr(error, "original"):
        if isinstance(error.original, HTTPException):
            await ctx.send("Unable to send message.")

        if isinstance(error.original, Forbidden):
            await ctx.send("I do not have permission to do that.")

        else:
            raise error.original

    else:
        raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)
