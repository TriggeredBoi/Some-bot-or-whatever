import discord
from discord.ext import commands
from Game.Player import Player
import Game.ServerTemplates as ST


class Playerdict(dict):
    def __init__(self, guild: discord.Guild):
        super().__init__(self)
        self.guild = guild
    
    async def add(self, member: discord.Member): #key by id instead maybe?
        if self.get(member):
            return
        self[member] = Player(member)
        #I plan on refactoring Player and make *it* handle adding roles; Remember to remove this later
        await member.add_roles(self.guild.player_role)
        await member.remove_roles(self.guild.ghost_role) #doesn't hurt to be redundant
    
    async def remove(self, player: Player):
        await player.member.remove_roles(self.guild.player_role, self.guild.ghost_role)
        del self[player.member]
        del player #should be garbage collected I'm pretty sure but eh

class Server:
    def __init__(self, server):
        self.guild = server 
        self.name = self.guild.name

        self.game_category = None
        self.game_channels = {} #{channel class: channel obj}
        self.game_roles = {}    #{role class: role obj}
        self.update_links()

        self.players = Playerdict(self.guild) #{member ID: player object}


    async def addplayer(self, member):
        if not self.players.get(member):
            await self.players.add(member) 
            return True
        else: return False
    

    async def removeplayer(self, member):
        if player := self.players.get(member):
            await self.players.remove(player) 
            return True
        else: return False


    def update_links(self):
        self.game_category = discord.utils.get(self.guild.categories, name='Town of Salem')
        
        self.game_channels = {}
        missingchannels = []
        for template in ST.AllGameChannels():
            if channel := discord.utils.get(self.guild.channels, name=template.name, category=template.category):
                pass #why the fuck can I not do "if not" with an assignment operator
            else:
                missingchannels.append(template)
            self.game_channels[template] = channel

        self.game_roles = {}
        missingroles = []
        for template in ST.AllGameRoles():
            if role := discord.utils.get(self.guild.roles, name=template.name):
                pass
            else:
                missingroles.append(template)
            self.game_channels[template] = role
        
        return missingchannels, missingroles


    async def setup(self, ctx):
        missingchannels, missingroles = self.update_links() #stuff may have been deleted, and the command is being called to fix them
        reason = f'Setup invoked by {ctx.message.author.name} in #{ctx.message.channel}.'
        result = ""
        #TODO: apply default permissions to each channel on setup
        if not self.game_category:
            self.game_category = await self.guild.create_category('Town of Salem',
                                                                  reason=reason)
            result+=f"""Created "{self.game_category.name}" category... (Discord will display it in full uppercase)\n"""

        for template in missingchannels:
            channel = await self.guild.create_text_channel(name=template.name, topic=template.topic, category=self.game_category, reason=reason)
            result+=f"Created {channel.mention}...\n"

        for template in missingroles:
            role = await self.guild.create_role(name=template.name, colour=template.color, hoist=template.hoist, reason=reason)
            result+=f"Created {role.mention}...\n"

        
        if result == "": await ctx.send("Nothing changed...")
        else:
            result+=f"""
Looks like we're done here!
Head to {self.game_channels[ST.LobbyChannel].mention}, do ``!join``, get 12 players, and get playing!

Admins:
- You may NOT move the created channels out of the "{self.game_category.name}" category.
- You may NOT rename any of these channels or roles. The bot will lose track of them.
- You MAY edit the channels however you want (except renaming them or moving them out of the category)
- You MAY edit the roles however you want. (again, except renaming them)
- HOWEVER, be aware that the bot will overwrite certain channel permissions for the game roles during the game.
- The game roles are set to display separately from other members - Change this at will.
- I've left a couple extra notes for you in most channels' descriptions - Read them, then delete them! Or not. I'm not your mom. You do you.
"""
            await ctx.send(result)
        
        

            #TODO: startgame() and endgame()

        
        
        
        
        
        
        
        