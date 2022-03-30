from string import punctuation, ascii_letters

from random import randint, choice, random

from time import time, sleep

Quests = False

#Roles

heroes = ("PERCY JACKSON","ELF","ZELDA")

goodNPCs = ("HEALER",)

badNPCs = {"NINJA":0.05,"OGRE":0.01, "DEMON":0.94}

places = ("HOUSE", "BEACH", "FOREST", "MOUNTAIN", "DESERT")

neutralNPCs = ("MINER", "WOODCHUCKER")





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

        # Task 1: Modify descriptions of inventory

        self.inventory = {"Cookie":{"Name":"Cookie", "Picture":"🍪", "Description":"Something to eat!", "Number":0},

                         "Logs":{"Name":"Logs", "Picture":"🪵", "Description":"Something you can use in the shop for crafting things or to sell", "Number":0},

                        "Sand":{"Name":"Sand", "Picture":"🟫", "Description":"Something you can smelt or sell!", "Number":0},

                       "Rocks":{"Name":"Rocks", "Picture":"🪨", "Description":"Something you can use in the shop for crafting things, selling, or refining", "Number":0},

                        "Silver":{"Name":"Silver", "Picture":"🪙", "Description":"Something you can use in the shop for crafting things, selling, or fusing","Number":0},

                        "Gold":{"Name":"Gold", "Picture":"⚱️", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0},

                        "Diamond":{"Name":"Diamond", "Picture":"💎", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0},

                        "Emerald":{"Name":"Emerald", "Picture":"🟩", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0},

                        "Cactus":{"Name":"Cactus", "Picture":"🌵", "Description":"Something to sell or turn into pointy armour!", "Number":0},

                        "Golden Sapling":{"Name":"Golden Sapling", "Picture":"🌸", "Description":"Grows into a golden tree!", "Number":0},

                        "Golden Log":{"Name":"Golden Log", "Picture":"🌴", "Description":"The most powerful wood, when combined with weapons +10 to all stats!", "Number":0}}



    def printInventory(self):

        for item in self.inventory:

            if self.inventory[item]["Number"] != 0:

                print("{} {} {:>10}".format(self.inventory[item]["Name"],self.inventory[item]["Picture"],"x "+str(self.inventory[item]["Number"])))

                print("Description:",self.inventory[item]["Description"])



       

    



# Task 1: complete the other hero classes to be like zelda





class PercyJackson(Role):

    def __init__(self, name):

        self.attackpower = 20

        self.health = 200

        self.defense = 0.0



class Elf(Role):

    def __init__(self, name):

        self.attackpower = 40

        self.health = 50

        self.defense = 0.0



class Zelda(Role):

    def __init__(self,name):

        super().__init__(name)

        self.picture = "🗡"

        self.attackpower = 20

        self.health = 100

        self.defense = 0.0



class NPC:

    pass

    

class GoodNPC(NPC):

    pass



class BadNPC(NPC):

    def __init__(self,name):

        global badNPCs, randint

        self.role = name

        if self.role == "NINJA":

            self.picture = "🥷"

            self.attackpower = 10

            self.health = 20

            self.defense = 0.5

        elif self.role == "OGRE":

            self.picture = "👹"

            self.attackpower = 10

            self.health = 100

            self.defense = 0.25

        elif self.role == "DEMON":

            self.picture = "👿"

            self.attackpower = 5

            self.health = 20

            self.defense = 0.2



class NeutralNPC(NPC):

    def __init__(self):

        global neutralNPCs, randint

        self.role = neutralNPCs[randint(0,len(neutralNPCs)-1)]

        self.picture = "⛏" if self.role=="MINER" else "🪓"

    

    





def Mine(role, setting):

    global time

    map()

    TheSetting = setting.name.upper()

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

        x = input("Enter '{}': (Type 'stop' to stop) ".format(randletter))

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

    

    

    #TASK 2: ADD DIFFERENT PROBABILITIES (AS IS DONE FOR MOUNTAIN) FOR THE OTHER SETTINGS

    if TheSetting == "BEACH":

        for i in range(points):

            role.inventory["Sand"]["Number"] += 1

        

    elif TheSetting == "FOREST":

        for i in range(points):

            Temprand = randint(1, 100)

            if 1 <= Temprand <= 2:

                role.inventory["Golden Sapling"]["Number"] += 1

            if 3 <= Temprand <=7:

                role.inventory["Golden Log"]["Number"] += 1

            else:

                role.inventory["Logs"]["Number"] += 1

        return

    elif TheSetting == "HOUSE":

        for i in range(points):

            role.inventory["Cookie"]["Number"] += 1

        

    elif TheSetting == "MOUNTAIN":

        for i in range(points):

            Temprand = randint(1,100)

            if 1 <= Temprand <= 25:

                role.inventory["Silver"]["Number"] += 1

            elif 26 <= Temprand <= 35:

                role.inventory["Gold"]["Number"] +=1

            elif 36 <= Temprand <= 40:

                role.inventory["Diamond"]["Number"] += 1

            elif 41 <= Temprand <= 42:

                role.inventory["Emerald"]["Number"] += 1

            else:

                role.inventory["Rocks"]["Number"] += 1

    elif TheSetting == "DESERT":

        for i in range(points):

            Temprand = randint(1, 100)

            if 1 <= Temprand <= 25:

                role.inventory["Cactus"]["Number"] += 1

            else:

                role.inventory["Sand"]["Number"] += 1

        



    print("The player average is {:.2f} seconds".format(playeravg/playeravglen))

    print("The bot average is {:.2f} seconds".format(botavg/botavglen))

    print("You got {} resources in total!".format(points))

    print("You won {} games!".format(wins))

    print("You lost {} games!".format(losses))

    print("{} is the number of games that drawed!".format(draws))

    

    return points



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

        option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

        while option not in ("MAP","SEARCH","QUESTS", "MINE", "INV"):

            print("Try again!")

            option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

        while option == "MAP" or option == "SEARCH" or option=="MINE" or option=="INV":

            if option == "MAP":

                setting.map()

                option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

                while option not in ("MAP","SEARCH","QUESTS", "MINE", "INV"):

                    print("Try again!")

                    option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

            elif option == "SEARCH":

                search(setting)

                option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

                while option not in ("MAP","SEARCH","QUESTS", "MINE", "INV"):

                    print("Try again!")

                    option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

            elif option == "MINE":

                Mine(role,setting)

                option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

                while option not in ("MAP","SEARCH","QUESTS", "MINE", "INV"):

                    print("Try again!")

                    option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

            elif option == "INV":

                role.printInventory()

                option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

                while option not in ("MAP","SEARCH","QUESTS", "MINE", "INV"):

                    print("Try again!")

                    option = cS(input("Enter either 'Map', 'Search', 'Mine', 'Inv' or 'Quests': "))

        

def Quest1(RoleHero):

    global badNPCs # we're saying that we will be using the global variable badNPCs

    NumberDefeated = 0

    while NumberDefeated <= 10 or RoleHero.health <= 0:

        randnum = randint(1,100)

        start = 1

        end = 0

        for b in badNPCs:

            end += int(badNPCs[b]*100)

            if start <= randnum <= end:

                a = BadNPC(b)

                RoleHero.health -= a.attackpower

                print(f"Player took {a.attackpower} damage!")

                pin = (int(input("What attack do you want to use?:\n 1: Quick Attack\nType here: ")))

                while pin != 1:

                    pin = (int(input("What attack do you want to use?:\n1: Quick Attack\nType here: ")))

                if pin == 1:

                    a.health -= RoleHero.attackpower

                    print(f"You did {RoleHero.attackpower} damage")

                # Task 2 (Optional): Simulate the fight between the RoleHero and the random BadNPC 'a'

            start += end

    

    

def HeroGame(playerhero):

    if playerhero == "PERCY JACKSON":

        RoleHero = PercyJackson(playerhero)

    elif playerhero == "ELF":

        RoleHero = Elf(playerhero)

    elif playerhero == "ZELDA":

        RoleHero = Zelda(playerhero)

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

        Place = Beach()

        Menu(RoleHero,Place)

    elif placetogo == "FOREST":

        Place = Forest()

        Menu(RoleHero,Place)

    elif placetogo == "MOUNTAIN":

        Place = Mountain()

        Menu(RoleHero,Place)

    elif placetogo == "DESERT":

        Place = Desert()

        Menu(RoleHero,Place)

    print("New thing unlocked! Quests have been unlocked.")

    global Quests

    Quests = True

    print("To open quests, in the menu quests will be unlocked.")

    Menu(RoleHero,Place)

    Quest1(RoleHero)

    

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