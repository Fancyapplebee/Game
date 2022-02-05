from string import punctuation
from random import randint
Quests = False
#Roles
heroes = ("PERCY JACKSON","ELF","ZELDA")
villains = ("ELF","GOBLIN")
goodNPCs = ("Healer",)
places = ("HOUSE", "BEACH", "FOREST", "MOUNTAIN", "DESERT")

def cS(s):
    return s.upper().translate(str.maketrans('', '', punctuation))
#Role Types
class Role():
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
        elif Quests == True:
            option = cS(input("Enter either 'Map', 'Search', or 'Quests'"))
        while option not in ("MAP","SEARCH","QUESTS"):
            print("Try again!")
            if Quests == False:
                option = cS(input("Enter either 'Map' or 'Search' "))
            elif Quests == True:
                option = cS(input("Enter either 'Map', 'Search', or 'Quests'"))
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

class NPC(Role):
    pass
    

class GoodNPC(NPC):
    pass

class BadNPC(NPC):
    pass

class NeutralNPC(NPC):
    pass



#Setting Types
class Setting:
    pass

class House(Setting):
    def __init__(self):
        self.name = "House"
        self.places = ("FRIDGE","BED","LIVINGROOM")

        
        
        

class Beach(Setting):
    def __init__(self,Role):
        self.name = "Beach"
        self.places = ("SAND, CASTLE, OCEAN") # Fill this up


class Forest(Setting):
    def __init__(self,Role):
        self.name = "Forest"
        self.places = ("TREE") # Fill this up


class Mountain(Setting):
    def __init__(self,Role):
        self.name = "Mountain"
        self.places = ("CAVE, UP") # Fill this up


class Desert(Setting):
    def __init__(self,Role):
        self.name = "Desert"
        self.places = ("SAND, CACTUS, WELL") # Fill this up



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
            RoleHero.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "BEACH":
        Place = Beach(RoleHero)#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            RoleHero.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "FOREST":
        Place = Forest(RoleHero)#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            RoleHero.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "MOUNTAIN":
        Place = Mountain(RoleHero)#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            RoleHero.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    elif placetogo == "DESERT":
        Place = Desert(RoleHero)#complete this to be like the first if-statement
        option = RoleHero.Menu1()
        if option=="MAP":
            RoleHero.map()
        elif option=="SEARCH":
            place = RoleHero.search(Place)
    print("New thing unlocked! Quests have been unlocked.")
    Quests = True
    print("To open quests, in the menu quests will be unlocked.")
    option = RoleHero.Menu1()
    
    
    
    
    

    
    
    
def VillainGame(playervillain):  # Make this be like HeroGame
    if playervillain == "ELF":
        RoleVillain=Elf(playervillain)
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
            RoleVillain.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "BEACH":
        Place = Beach(RoleVillain)#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            RoleVillain.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "FOREST":
        Place = Forest(RoleVillain)#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            RoleVillain.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "MOUNTAIN":
        Place = Mountain(RoleVillain)#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            RoleVillain.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)
    elif placetogo == "DESERT":
        Place = Desert(RoleVillan)#complete this to be like the first if-statement
        option = RoleVillain.Menu1()
        if option=="MAP":
            RoleVillain.map()
        elif option=="SEARCH":
            place = RoleVillain.search(Place)

    

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