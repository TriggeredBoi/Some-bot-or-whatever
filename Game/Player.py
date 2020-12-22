import discord
import Game.Roles as Roles

class Player:
    def __init__(self, member: discord.Member):
        self.member = member
        self.name = member.display_name
        self.server = member.guild #the parent server ref the Player belongs to
        
        self.role = Roles.Default(self)
        self.listening = False


    async def kill(self):
        await self.member.remove_roles(self.server.player_role)
        await self.member.add_roles(self.server.ghost_role)