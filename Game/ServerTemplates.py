import discord

class BaseChannelTemplate():
    name = "oopsie whoopsie"
    topic = None
    category = "Town of Salem"

    #here is where I wish python wasn't entirely a runtime language, I can't reference the roles in the class' definition because they weren't defined yet
    #so this code is gonna have to be hackier than I wanted it to.
    def __init__(self):
        #{role: discord.PermissionOverwrite} (a role's channel_permissions will be applied after this, so it will take precedence)
        self.role_permissions = {
            everyone: discord.PermissionOverwrite(
                read_messages=False,
                send_messages=False,
                read_message_history=False,
            ),

            GhostRole: discord.PermissionOverwrite(
                send_messages=False,
            ),
        }
        #self.job_permissions = {}

        self.init_permissions()

    def init_permissions(self):
        pass

    def find(self, guild):
        return discord.utils.get(guild.text_channels, name=self.name, category=self.category)

def AllGameChannels():
    return BaseChannelTemplate.__subclasses__()

class LobbyChannel(BaseChannelTemplate):
    name = "lobby"
    topic = "This is the lobby channel, use the \"join\" and \"leave\" commands. This channel is not meant for communication about the current game. Moderators should punish players accordingly."
    def init_permissions(self):
        self.role_permissions.update({
            everyone: discord.PermissionOverwrite(), #reset perms, this one should be visible
            PlayerRole: discord.PermissionOverwrite(send_messages=False),
            GhostRole: discord.PermissionOverwrite(send_messages=False),
            })

class VillageChannel(BaseChannelTemplate):
    name = "village"
    topic = "This is the village channel. It unlocks during the day so discussion and voting may happen."
    def init_permissions(self):
        self.role_permissions.update({
            PlayerRole: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            ),
            GhostRole: discord.PermissionOverwrite(
                read_messages=True,
            ),
            SpectatorRole: discord.PermissionOverwrite(
                read_messages=True
            ),
            })

class GraveyardChannel(BaseChannelTemplate):
    name = "graveyard"
    topic = "This is the graveyard channel. When you are dead, you can usually only talk in here. But don't leave just yet - A Medium can still reach out to you, or you could be revived by a Retributionist!"
    def init_permissions(self):
        self.role_permissions.update({
            GhostRole: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            ),
            SpectatorRole: discord.PermissionOverwrite(
                read_messages=True
            ),
            })

class MafiaChannel(BaseChannelTemplate):
    name = "hideout"
    topic = "This is the mafia channel. It unlocks during the night so the mafia members may decide on a victim."


class BaseRoleTemplate():
    name = "oh noes"
    color = discord.Colour.default()
    hoisted = False #displayed separately from others and etc
    channel_permissions = {} #{channeltemplate: discord.PermissionOverwrite}

    def find(self, guild):
        return discord.utils.get(guild.roles, name=self.name)

def AllGameRoles():
    return BaseRoleTemplate.__subclasses__()

class everyone():
    def find(self, guild): #won't be created, but it's find() method will be called
        return guild.roles[0] #@everyone will always be index 0

class PlayerRole(BaseRoleTemplate):
    name = "Player"
    color = discord.Colour.blue()

class GhostRole(BaseRoleTemplate):
    name = "Ghost"
    color = discord.Colour.lighter_grey()

class LobbyRole():
    name= "In lobby"

class SpectatorRole(BaseRoleTemplate):
    name = "Spectator"

#lobby role? or keep changing player role perms?