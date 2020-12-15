from discord.ext import commands

def setup(bot):
    bot.add_cog(gamecogs(bot))
    print("gamecogs loaded")


def findserverobj(query, serverlist):
    if type(query) == commands.context.Context: query = query.guild
    
    for server in serverlist:
        if server.guild == query: return server
    
    print(f"findserverobj failed to do its job. Query: {query} (Type: {type(query)})")
    return False

class gamecogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.serverlist = bot.serverlist
        #actually nah, even though bot doesn't have serverlist by default, if it didn't manage to create bot.serverlist something's already fucked up royally
    
    @commands.command()
    async def join(self, ctx):
        server = findserverobj(ctx, self.bot.serverlist)
        
        if await server.addplayer(ctx.message.author): await ctx.send(f"{ctx.message.author.mention}, you have joined the queue.")
        else: await ctx.send("You're already in the queue, dummy.")
    
    
    @commands.command()
    async def leave(self, ctx):
        server = findserverobj(ctx, self.bot.serverlist)
        
        if await server.removeplayer(ctx.message.author): await ctx.send(f"{ctx.message.author.mention}, you have left the queue.")
        else:
            await ctx.message.author.remove_roles(server.player_role, server.ghost_role) #just in case
            await ctx.send("You're not in the queue, dummy.")
    
    @commands.command()
    async def queue(self, ctx):
        server = findserverobj(ctx, self.bot.serverlist)
        if len(server.playerlist) == 0:
            await ctx.send("The queue is empty!")
            return
    
        if len(server.playerlist) == 1:
            await ctx.send(f"**{server.playerlist[0].member.display_name}** is the sole player in the queue.\nCome on, don't leave them alone like that; ``!join`` them!")
            return
    
        message = (f"There are **{len(server.playerlist)}** players in the queue:\n")
        for player in server.playerlist:
            message = message + (f"- **{player.member.display_name}**\n")
        await ctx.send(message)
        return
            
        
        
        
        
        
 
    

        