import json
import re
import math

def check4arg(argsgiven, targetarg):
    if targetarg in argsgiven: return True
    else: return False
    
    
def emote_to_emoteref(string): #don't touch this. ever. it works. I don't know for sure how. leave it be.
    with open("emotes.json") as stufftoread:
        emotedict = json.load(stufftoread)

    for item in emotedict.keys():
        string = re.sub(item, emotedict[item], string)
    return string


def round_up(n, decimals=0):                #https://www.knowledgehut.com/blog/programming/python-rounding-numbers
    multiplier = 10 ** decimals             #What? I don't like math. So that's why I copy algorithms off of others. Blame bad math teachers, not me.
    return math.ceil(n * multiplier) / multiplier


def to_int(target): #tries to convert to an int. if it fails, it won't generate an annoying-ass exception. it will return the unconverted argument instead of a nonetype. 
    try: return int(target)
    except: return target


def yeetfirstword(yeetstring):       #past trigg, what the shit is this
    yeetlist = yeetstring.split(" ") #transform the string into a list
    del yeetlist[0]                  #YEET index 0 (the first word)
    return " ".join(yeetlist)        #return the YEETED string


"""
def makefactionnamecool(string): #very cool
    with open("factionthingies.json") as stufftoread:
        emotedict = json.load(stufftoread)

    for item in emotedict.keys():
        string = re.sub(item, emotedict[item], string) #http://pythoninthewyld.com/2018/03/12/dict-based-find-and-replace-deluxe/
    return string
"""