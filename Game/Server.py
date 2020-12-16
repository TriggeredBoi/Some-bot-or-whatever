import discord
from discord.ext import commands
from Game.Player import Player



class playerdict(dict):
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


class Server:
    def __init__(self, server):
        self.guild = server 
        self.name = self.guild.name

        self.update_links()

        """ bad. horrible. horrendous. terrible. absolutely disgusting.
        self.userlist = []   #should be always parallel to playerlist, except hold member refs instead of player objects for easy comparison in stuff like addplayer
        self.playerlist = custom_playerlist_list(self) #every addition to playerlist SHOULD automatically update userlist
        #REMINDER: do not directly manipulate userlist because of the above.
        """
        self.players = playerdict(self.guild) #{member ID: player object}


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
        
        
        self.lobby_channel = discord.utils.get(self.guild.channels, name="lobby", category=self.game_category)
        
        self.graveyard_channel = discord.utils.get(self.guild.channels, name="graveyard", category=self.game_category)
        
        self.village_channel = discord.utils.get(self.guild.channels, name="village", category=self.game_category)
        
        self.mafia_channel = discord.utils.get(self.guild.channels, name="hideout", category=self.game_category)
        
        
        self.player_role = discord.utils.get(self.guild.roles, name="Player")
        
        self.ghost_role = discord.utils.get(self.guild.roles, name="Ghost")


    async def setup(self, ctx):
        self.update_links() #stuff may have been deleted, and the command is being called to fix them
        reason = f'Setup invoked by {ctx.message.author.name} in #{ctx.message.channel}.'
        result = ""
        #TODO: apply default permissions to each channel on setup
        if not self.game_category:
            self.game_category = await self.guild.create_category('Town of Salem',
                                                                  reason=f'{reason} Admins - do not rename this category, or else the bot will forget it exists. You may move it at will, however.')
            result+=f"""Created "{self.game_category.name}" category... (Discord will display it in full uppercase)\n"""

        if not self.lobby_channel:
            self.lobby_channel = await self.guild.create_text_channel('lobby',
                                                                      topic="""This is the lobby channel, use the "join" and "leave" commands. Admins - Do not rename. Also, this channel is not meant for communication about the current game. Punish players accordingly.""",
                                                                      category=self.game_category,
                                                                      reason=reason)
            result+=f"Created {self.lobby_channel.mention}...\n"

        if not self.graveyard_channel:
            self.graveyard_channel = await self.guild.create_text_channel('graveyard',
                                                                      topic="This is the graveyard channel. When you are dead, you can usually only talk in here. But don't leave just yet - A Medium can still reach out to you, or you could be revived by a Retributionist!",
                                                                      category=self.game_category,
                                                                      reason=reason)
            result+=f"Created {self.graveyard_channel.mention}...\n"
        
        if not self.village_channel:
            self.village_channel = await self.guild.create_text_channel('village',
                                                                        topic='This is the village channel. It unlocks during the day so discussion and voting may happen. Admins - Do not rename.',
                                                                        category=self.game_category,
                                                                        reason=reason)
            result+=f"Created {self.village_channel.mention}...\n"
            
        if not self.mafia_channel:
            self.mafia_channel = await self.guild.create_text_channel('hideout',
                                                                      topic='This is the mafia channel. It unlocks during the night so the mafia members may decide on a victim. Admins - Do not rename.',
                                                                      category=self.game_category,
                                                                      reason=reason)
            result+=f"Created {self.mafia_channel.mention}...\n"
        
        if not self.player_role:
            self.player_role = await self.guild.create_role(name='Player', colour = discord.Colour.blue(), hoist = True, reason=reason)
            
            result+=f"Created {self.player_role.mention}...\n"
            
        if not self.ghost_role:
            self.ghost_role = await self.guild.create_role(name='Ghost', colour = discord.Colour.lighter_grey(), hoist = True, reason=reason)
            
            result+=f"Created {self.ghost_role.mention}...\n"
        
        if result == "": await ctx.send("Nothing changed...")
        else:
            result+=f"""
Looks like we're done here!
Head to {self.lobby_channel.mention}, do ``!join``, get 12 players, and get playing!

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

        
        
        
        
        
        
        
        