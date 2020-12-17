import discord

class BaseChannelTemplate():
    name = "oopsie whoopsie"
    topic = None
    category = "Town of Salem"
    #permissions = {role:[perms]} (a role's channel_permissions will be applied after this, so it will take precedence. decide where you'll define its perms.)

def AllGameChannels():
    return BaseChannelTemplate.__subclasses__()

class LobbyChannel(BaseChannelTemplate):
    name = "lobby"
    topic = "This is the lobby channel, use the \"join\" and \"leave\" commands. This channel is not meant for communication about the current game. Admins, punish players accordingly."

class GraveyardChannel(BaseChannelTemplate):
    name = "graveyard"
    topic = "This is the graveyard channel. When you are dead, you can usually only talk in here. But don't leave just yet - A Medium can still reach out to you, or you could be revived by a Retributionist!"

class VillageChannel(BaseChannelTemplate):
    name = "village"
    topic = "This is the village channel. It unlocks during the day so discussion and voting may happen."

class MafiaChannel(BaseChannelTemplate):
    name = "hideout"
    topic = "This is the mafia channel. It unlocks during the night so the mafia members may decide on a victim."


class BaseRoleTemplate():
    name = "oh noes"
    color = None
    hoisted = False #displayed separately from others and etc
    #permissions = soon:tm:?
    #channel_permissions = {channel:[perms]}

def AllGameRoles():
    return BaseRoleTemplate.__subclasses__()

class PlayerRole(BaseRoleTemplate):
    name = "Player"
    color = discord.Colour.blue()

class GhostRole(BaseRoleTemplate):
    name = "Ghost"
    color = discord.Colour.lighter_grey()

#lobby role? or keep changing player role perms?