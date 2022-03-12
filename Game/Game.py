from _typeshed import SupportsKeysAndGetItem
from string import punctuation, ascii_letters
from random import randint, choice, random
from time import time, sleep
Quests = False
#Roles
heroes = ("PERCY JACKSON","ELF","ZELDA")
villains = ("ELF","GOBLIN")
goodNPCs = ("HEALER",)
places = ("HOUSE", "BEACH", "FOREST", "MOUNTAIN", "DESERT")
neutralNPCS = ("MINER", "WOODCHUCKER")

#Zeeshan Rizvi
#https://stackoverflow.com/questions/17432478/python-print-to-one-line-with-time-delay-between-prints/52595545#52595545?newreg=cb618a4b6ed14f8bb7a782e731f4c678
def slowPrint(text):
    for i in text:
        print(i, end='', flush=True)
        sleep(0.15)
    print()

def cS(s):
    return s.upper().translate(str.maketrans('', '', punctuation))
    

#Role Types
class Role:
    def __init__(self, name):
        self.name = name
        self.inventory = [{"Name":"Logs", "Picture":"🪵", "Description":"Something you can use in the shop for crafting things", "Number":0}, ]
    def printInventory(self):
        for item in self.inventory:
            if item["Number"] != 0:
                print("{} {} {:>10}".format(item["Name"],item["Picture"],"x "+str(item["Number"])))
                print("Description:",item["Description"])

       
    

class Hero(Role):
    pass

class Villain(Role):
    pass

class PercyJackson(Hero):

    pass

class Elf(Hero, Villain):
    pass

class Zelda(Hero):
    pass

class Goblin(Villain):
    pass

class NPC(Role):
    pass
    

class GoodNPC(NPC):
    pass

class BadNPC(NPC):
    pass

class NeutralNPC(NPC):
    def __init__(self):
        global neutralNPCS, randint
        self.role = neutralNPCS[randint(0,1)]
        self.picture = "⛏" if self.role=="MINER" else "🪓"
    
    

# Task 1: modify the Menu function so that the user can print their inventory
# Task 2: pass a setting variable to Mine, and, depending on the setting, they
# can have the possibility to mine different items

def Mine(Setting):
    global time
    print("The objective of this game is to type the letter in time (To stop, type stop)!")
    Opponent = NeutralNPC()
    print(f"Get ready, you are about to face the {Opponent.role} {Opponent.picture}")
    wins = 0
    losses = 0
    draws = 0
    totalplayerscore = 0
    playeravg = []
    botavg = []
    avgtime = []
    while True:
        start = time()
        randletter = choice(ascii_letters)
        x = input("Enter '{}': ".format(randletter))
        if cS(x)=="STOP":
            break
        stop = time()
        Time = (stop-start)
        print("You entered it in {:.2f} seconds!".format(Time))
        npcTime = 1+(3*random())

        if Time < npcTime and x==randletter:
            print("You passed!")
            wins+=1
            totalplayerscore += 1
            botavg.append(npcTime)
            playeravg.append(Time)
        elif Time > npcTime or x!=randletter:
            print("You lost!")
            losses +=1
            totalplayerscore -= 1
            botavg.append(npcTime)
            playeravg.append(Time)
        elif Time == npcTime:
            print("Draw")
            draws+=1
            botavg.append(npcTime)
            playeravg.append(Time)
    playeravglen = (len(playeravg))
    playeravg = sum(playeravg)
    botavglen = (len(botavg))
    botavg = sum(botavg)
    points = wins - losses
    if playeravg/playeravglen < botavg/botavglen:
        print("You get 5 extra resources because your avg was better than the bot!")
        points += 5
    elif Setting == "BEACH":
        Sand = Sand 
        Sand += Points
    elif Setting == "FOREST":

    elif Setting == "MOUNTAIN":

    elif Setting == "DESSERT":

    print("The player average is {:.2f} seconds".format(playeravg/playeravglen))
    print("The bot average is {:.2f} seconds".format(botavg/botavglen))
    print("You got {} resources in total!".format(points))
    print("You won {} games!".format(wins))
    print("You lost {} games!".format(losses))
    print("{} is the number of games that drawed!".format(draws))
    
    return points
    
    #Give the player 5 bonus points if the player's average is better than the npc.
     # Print out the statistics, wins, losses, draws, average time of the player, average time of the npc, points that the player won, i.e., points = wins-losses
    

#Setting Types
class Setting:
    def map(self):
        print("------")
        print("Places")
        print("------")
        for place in self.places:
            print(place)
        print()

class House(Setting):
    def __init__(self):
        self.name = "House"
        self.places = ("FRIDGE","BED","LIVINGROOM")

        
        
    
class Beach(Setting):
    def __init__(self):
        self.name = "Beach"
        self.places = ("SAND", "CASTLE", "OCEAN") # Fill this up


class Forest(Setting):
    def __init__(self):
        self.name = "Forest"
        self.places = ("TREE",) # Fill this up


class Mountain(Setting):
    def __init__(self):
        self.name = "Mountain"
        self.places = ("CAVE", "UP") # Fill this up


class Desert(Setting):
    def __init__(self):
        self.name = "Desert"
        self.places = ("SAND", "CACTUS", "WELL") # Fill this up



def displayHeroes():
    print("------")
    print("Heroes")
    print("------")
    for hero in heroes:
        print(hero)
    print()
    
def displayVillains():
    print("------")
    print("Villains")
    print("------")
    for villain in villains:
        print(villain)
    print()
    

def map():
    print("------")
    print("Places")
    print("------")
    for place in places:
        print(place)
    print()

def search(setting):
    print("------")
    print("Places")
    print("------")
    for place in setting.places:
        print(place)
    print("------")
    place = cS(input(f"Where in the {setting.name} do you want to explore? "))
    while place not in setting.places:
        print("Try again!")
        place = cS(input(f"Where in the {setting.name} do you want to explore? "))
    return place

def Menu(role, setting):
    if Quests == False:
        option = cS(input("Enter either 'Map' or 'Search' "))
        while option not in ("MAP","SEARCH"):
            print("Try again!")
            option = cS(input("Enter either 'Map' or 'Search' "))
        if option == "MAP":
            setting.map()
        elif option == "SEARCH":
            search(setting)
    elif Quests == True:
        option = cS(input("Enter either 'Map', 'Search', 'Mine' or 'Quests'(To print your inventory type 'PrintInv'"))
        while option not in ("MAP","SEARCH","QUESTS", "MINE", "PRINTINV"):
            print("Try again!")
            option = cS(input("Enter either 'Map', 'Search', 'Mine' or 'Quests'(To print your inventory type 'PrintInv'")) 
        while option == "MAP" or option == "SEARCH" or option=="MINE":
            if option == "MAP":
                setting.map()
                option = cS(input("Enter either 'Map', 'Search', 'Mine' or 'Quests'(To print your inventory type 'PrintInv'"))
            elif option == "SEARCH":
                search(setting)
                option = cS(input("Enter either 'Map', 'Search', 'Mine' or 'Quests'(To print your inventory type 'PrintInv'"))
            elif option == "MINE":
                role.inventory[0]["Number"] += Mine()
                option = cS(input("Enter either 'Map', 'Search', 'Mine' or 'Quests'(To print your inventory type 'PrintInv'"))
            elif option == "PRINTINV":
                printInventory 

    
    
def HeroGame(playerhero):
    if playerhero == "PERCY JACKSON":
        RoleHero = PercyJackson(playerhero)
    elif playerhero == "ELF":
        RoleHero = Elf(playerhero)
    elif playerhero == "ZELDA":
        RoleHero = Zelda(playerhero)
    Sand = 0
    Logs = 0
    Rocks = 0
    Silver = 0
    Gold = 0
    Diamond = 0
    Emerald = 0
    print("Where am I?")
    print("You see a chest.")
    open = cS(input("Do you open the chest? "))
    while open != "YES" and open != "NO":
        print("Try again")
        open = cS(input("Do you open the chest? "))
    if open == "YES":
        print("You do not have the key.")
    elif open == "NO":
        print("You continue on with your day.")
    map()
    placetogo = cS(input("Where do you want to go? "))
    while placetogo not in places:
        print("Try again")
        placetogo = cS(input("Where do you want to go? "))
    print("Going to {}".format(placetogo))
    print(f"You are now at {placetogo}")
    if placetogo == "HOUSE":
        Place = House()
        Menu(RoleHero,Place)
    elif placetogo == "BEACH":
        Place = Beach()#complete this to be like the first if-statement
        Menu(RoleHero,Place)
    elif placetogo == "FOREST":
        Place = Forest()#complete this to be like the first if-statement
        Menu(RoleHero,Place)
    elif placetogo == "MOUNTAIN":
        Place = Mountain()#complete this to be like the first if-statement
        Menu(RoleHero,Place)
    elif placetogo == "DESERT":
        Place = Desert()#complete this to be like the first if-statement
        Menu(RoleHero,Place)
    print("New thing unlocked! Quests have been unlocked.")
    global Quests
    Quests = True
    print("To open quests, in the menu quests will be unlocked.")
    Menu(RoleHero,Place)
    RoleHero.printInventory()
        
    
#    New Game
# 5x6 grid numbers from 1 to 30
#
#
#
#
#
#
#
#
#
#
#
#
#
#
    


    

def game():
    slowPrint("Welcome to the Game!")
#    Animation
    displayHeroes()
    playerhero = cS(input("What hero do you want to be? "))
    while playerhero not in heroes:
        print("Error: Please try again")
        playerhero = cS(input("What hero do you want to be? "))
    HeroGame(playerhero)


    
'''
health system for all the roles,
damage system for all the roles,
item system for all the roles,
    special items for special roles:
        examples:
        - Percy Jackson's riptide
        - Elf's elf key
        - Zelda has a special bow and a sword
damage multiplier, armor, ...
'''



game()