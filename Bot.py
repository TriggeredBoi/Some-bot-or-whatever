import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from random import choice
from Game.Server import Server

load_dotenv() #get the token from the .env file. I was told this is a good idea because SECRECY
token = os.getenv("DISCORD_TOKEN")

#bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), case_insensitive = True)
global bot
bot = commands.Bot(command_prefix="$", case_insensitive = True)
print(f"Bot prefix: {bot.command_prefix}")

initiated = False

#bot.serverlist = []
bot.gameservers = {} #{guild id: server object}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("with Werewolves!"))
    
    if not initiated: #sometimes discord dies. make sure we don't reset the server objects when it comes back up.
        for guild in bot.guilds:
            print(f"Initializing {guild}...")
            #bot.serverlist.append(Server(guild))

            if not bot.gameservers.get(guild):
                bot.gameservers[guild.id] = Server(guild)
    
    print("Bot is up.")



unknown_command_list = ["What?", "wat", "Excuse me WHAT", "The fuck does that mean?", "I don't speak dumbanese."]
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("Stop spamming my dms you dipshit")
        return

    if isinstance(error, commands.CommandNotFound):
        if not ctx.message.guild: #will return FALSE if there is no guild.
            await ctx.send("Stop spamming my dms you dipshit") #complain about spamming my dms instead of saying it's not a command
            return

        await ctx.send(choice(unknown_command_list)) #wat?
        return

    if isinstance(error, commands.MissingRole):
        await ctx.send("FOOL! Only Moderators can use this command.")
        return

    if isinstance(error, commands.BadArgument):
        await ctx.send("The fuck is that argument mate")
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Y'know, if you actually gave me an argument I would have done something.")
        return

    raise error


def findserverobj(ctx): #returns a Server object from a context
    if server := bot.gameservers.get(ctx.guild.id):
        return server
    else:
        raise AssertionError
    return None

@bot.command()
async def setup(ctx):
    await findserverobj(ctx).setup(ctx)
    
    
cogpaths = [
    "cogs.Gimmicks",
    "Game.Gamecogs",
]

@bot.command()
async def reload(ctx):
    for cog in cogpaths:
        bot.reload_extension(cog)
    await ctx.send("Done.")


for cog in cogpaths:
    bot.load_extension(cog)

bot.run(token)