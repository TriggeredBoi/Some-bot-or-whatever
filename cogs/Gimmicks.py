from discord.ext import commands
from random import choice

def setup(bot):
    bot.add_cog(Gimmicks(bot))
    print("Gimmicks loaded")




class Gimmicks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = ["erp", "yiff", "uwu", "owo", "beastars", "legosi", "haru", "juno", ">w<", ">o<", "WGW"]
    
    
    
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        
        #self reactions
        if message.author == self.bot.user: 
            
            if message.content == "<a:hedance:670104985643515934>": #add :hedance: reaction when the bot says :hedance: on a messaage
                if not message.guild: return #don't react to itself on DMS
                await message.add_reaction("<a:hedance:670104985643515934>")
        
        return #no more infinite loops on my watch
        
        #reactions to users
        for item in self.bad_words:
            if item in str.lower(message.content):
                #await message.channel.send("fucking furry REEEEEEE")
                await message.add_reaction(choice(["<:woke:669278049581269012>", "<:bad:669373444802215956>"]))
            
        if "why won't you die" in str.lower(message.content) or "why wont you die" in str.lower(message.content):
            await message.channel.send("**NANOMACHINES, SON**")
            
        if message.author.id == 258621730833039360 and "unga" in str.lower(message.content): #this ID is Stalin's.
            await message.author.create_dm()
            await message.author.dm_channel.send("dunga")
            
        if message.content == ":3":
            await message.channel.send(":3")
       
        
        
        