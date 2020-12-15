#import discord
import Utils


class Default: #base role. does jack shit. other roles inherit from it. no one should ever have it.
    def __init__(self, player):
        self.playerobj = player
        self.player = self.playerobj.member
        self.server = self.playerobj.server
        self.name = "You shouldn't be able to see this."
        
        self.faction = "None"
        self.alignment = "None" #Town, Mafia, Neutral or Coven
        
        self.attack = 0
        self.defense = 0
    
    
    async def introduce(self):
        pass
    
    async def handleDM(self):
        pass

    async def dayaction(self):
        pass
    
    async def nightaction(self):
        pass

class Villager(Default):
    def __init__(self, player):
        super.__init__(player)
        
        self.name = "Villager"
        
        self.faction = "Town"
        self.alignment = "Benign"
    
    async def introduce(self):
        await self.player.create_dm()
        intromessage = f"**You are a Villager!**\nVillagers do not actually exist in Town of salem. They're just a basic placeholder for now."

        await self.player.send(Utils.emote_to_emoteref(intromessage))
        return True
    
    

class Vigilante(Default):
    def __init__(self, player):
        super.__init__(player)

        self.name = "Vigilante"
        
        self.faction = "Town"
        self.alignment = "Benign"
        
    async def introduce(self):
        await self.player.create_dm()
        intromessage = f"**You are a Vigilante!**\nChoose to take justice in your own hands and shoot someone. If you shoot a Townie, you will commit suicide over the guilt the next night. You only have 3 bullets. You cannot shoot a player on the first night."

        await self.player.send(Utils.emote_to_emoteref(intromessage))
        return True


class Mafioso(Default):
    def __init__(self, player):
        super.__init__(player)
        
        self.name = "Mafioso"
        
        self.faction = "Mafia"
        self.alignment = "Evil"
    
    async def introduce(self):
        await self.player.create_dm()
        intromessage = f"**You are a Mafioso!**\nChoose a target to kill at night. If there is a Godfather, anyone they pick overrides your decision. Become the new Godfather if the current one is killed."

        await self.player.send(Utils.emote_to_emoteref(intromessage))
        return True
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        