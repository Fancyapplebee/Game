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


def cS(s):
    return s.upper().translate(str.maketrans('', '', punctuation))
#Role Types
class Role:
    def __init__(self, name):
        self.name = name
    def map(self):
        print("------")
        print("Places")
        print("------")
        for place in places:
            print(place)
        print()
    def search(self, setting):
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
    
    def Menu1(self):
        if Quests == False:
            option = cS(input("Enter either 'Map' or 'Search' "))
            while option not in ("MAP","SEARCH"):
                print("Try again!")
                option = cS(input("Enter either 'Map' or 'Search' "))
        elif Quests == True:
            option = cS(input("Enter either 'Map', 'Search', 'Mine' or 'Quests' "))
            while option not in ("MAP","SEARCH","QUESTS", "MINE"):
                print("Try again!")
                if Quests == False:
                    option = cS(input("Enter either 'Map' or 'Search' "))
                elif Quests == True:
                    option = cS(input("Enter either 'Map', 'Search', 'Mine' or 'Quests' "))
        
        return option

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
    pass
    


def Mine():
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
    if playeravg/playeravglen > botavg/botavglen:
        print("You get 5 extra points because your avg was better than the bot!")
        points += 5
    print("The player average is {:.2f} seconds".format(playeravg/playeravglen))
    print("The bot average is {:.2f} seconds".format(botavg/botavglen))
    print("You got {} points in total!".format(points))
    print("You won {} games!".format(wins))
    print("You lost {} games!".format(losses))
    print("{} is the number of games that drawed!".format(draws))

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
    

    
    
def HeroGame(playerhero):
    if playerhero == "PERCY JACKSON":
        RoleHero = PercyJackson(playerhero)
    elif playerhero == "ELF":
        RoleHero = Elf(playerhero)
    elif playerhero == "ZELDA":
        RoleHero = Zelda(playerhero)
    print("Welcome to the game!")
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
    RoleHero.map()
    placetogo = cS(input("Where do you want to go? "))
    while placetogo not in places:
        print("Try again")
        placetogo = cS(input("Where do you want to go? "))
    print("Going to {}".format(placetogo))
    print(f"You are now at {placetogo}")
    if placetogo == "HOUSE":
        Place = House()
        option = RoleHero.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "BEACH":
        Place = Beach()#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "FOREST":
        Place = Forest()#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "MOUNTAIN":
        Place = Mountain()#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "DESERT":
        Place = Desert()#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    print("New thing unlocked! Quests have been unlocked.")
    global Quests
    Quests = True
    print("To open quests, in the menu quests will be unlocked.")
    option = RoleHero.Menu1()
    if option == "QUESTS":
        print("Quest 1: Chop Down 10 Trees")
        print("To chop down trees do the command 'Mine'")
        option = RoleHero.Menu1()
        if option == "MINE":
            Mine()
    
    
    
    

def VillainGame(playervillain):  # Make this be like HeroGame
    if playervillain == "ELF":
        RoleVillain= Elf(playervillain)
    elif playervillain == "GOBLIN":
        RoleVillain = Goblin(playervillain)
    print("Welcome to the game!")
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
    RoleVillain.map()
    placetogo = cS(input("Where do you want to go? "))
    while placetogo not in places:
        print("Try again")
        placetogo = cS(input("Where do you want to go? "))
    print("Going to {}".format(placetogo))
    print(f"You are now at {placetogo}")
    if placetogo == "HOUSE":
        Place = House()
        option = RoleVillain.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "BEACH":
        Place = Beach()#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "FOREST":
        Place = Forest()#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "MOUNTAIN":
        Place = Mountain()#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "DESERT":
        Place = Desert()#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            Place.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    #Complete this to be like the herogame function, but different, as this is for villains!
    

def game():
    
    Role = cS(input("Welcome! Are you are a hero or a villain? "))
    while Role!="HERO" and Role!="VILLAIN":
        Role = cS(input("Please enter 'Hero' or 'Villain': "))
    if Role=="HERO":
        displayHeroes()
        playerhero = cS(input("What hero do you want to be? "))
        while playerhero not in heroes:
            print("Error: Please try again")
            playerhero = cS(input("What hero do you want to be? "))
        HeroGame(playerhero)
    else:
        displayVillains()
        playervillain = cS(input("What villain do you want to be? "))
        while playervillain not in villains:
            print("Error: Please try again")
            playervillain = cS(input("What villain do you want to be? "))
        VillainGame(playervillain)
    

    
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