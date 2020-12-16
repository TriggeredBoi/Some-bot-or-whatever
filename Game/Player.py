import discord
import Game.Roles as Roles

class Player:
    def __init__(self, user: discord.Member):
        self.member = user
        self.name = self.member.display_name
        self.server = self.member.guild #the parent server ref the Player belongs to
        self.servername = self.server.name #the user-friendly name of the server
        
        self.role = Roles.Default(self)
        self.listening = False


    async def kill(self):
        await self.member.remove_roles(self.server.player_role)
        await self.member.add_roles(self.server.ghost_role)