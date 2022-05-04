from string import punctuation, ascii_letters
from random import randint, choice, random
from time import time, sleep
from inputimeout import inputimeout, TimeoutOccurred
Quests = False
#Roles
heroes = ("PERCY JACKSON","ELF","ZELDA")
goodNPCs = ("HEALER",)
badNPCs = {"NINJA":0.05,"OGRE":0.01, "DEMON":0.94}
places = ("HOUSE", "BEACH", "FOREST", "MOUNTAIN", "DESERT")
neutralNPCs = ("MINER", "WOODCHUCKER")


def Defense(Def):
    return 1-(Def/(Def+100))
#Zeeshan Rizvi
#https://stackoverflow.com/questions/17432478/python-print-to-one-line-with-time-delay-between-prints/52595545#52595545?newreg=cb618a4b6ed14f8bb7a782e731f4c678
def slowPrint(text):
    for i in text:
        print(i, end='', flush=True)
        sleep(0.15)
    print()

def cS(s):
    marksremoved = s.upper().translate(str.maketrans('', '', punctuation))
    return marksremoved.strip()

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
        "Diamond":{"Name":"Diamond", "Picture":"💎", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0}, "Emerald":{"Name":"Emerald", "Picture":"🟩", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0}, "Cactus":{"Name":"Cactus", "Picture":"🌵", "Description":"Something to sell or turn into pointy armour!", "Number":0},
        "Golden Sapling":{"Name":"Golden Sapling", "Picture":"🌸", "Description":"Grows into a golden tree!", "Number":0},
        "Golden Log":{"Name":"Golden Log", "Picture":"🌴", "Description":"The most powerful wood, when combined with weapons +10 to all stats!", "Number":0},
        "Sand Pail":{"Name":"Sand Pail", "Picture":"N/A","Description":"A bucket, maybe you can plant something in here.","Number":0},
        "Sand":{"Name":"Sand", "Picture":"⌛","Description":"Sand, used for smelting into glass or for making sandpaper.","Number":0}}
        self.defending = False
        
#    https://hypixel-skyblock.fandom.com/wiki/Defense
    def attack(self,enemy):
        enemy.health -= (Defense(enemy.defense)*self.attackpower)
        
    def printInventory(self):
        for item in self.inventory:
            if self.inventory[item]["Number"] != 0:
                print("{} {} {:>10}".format(self.inventory[item]["Name"],self.inventory[item]["Picture"],"x "+str(self.inventory[item]["Number"])))
                print("Description:",self.inventory[item]["Description"])


       
    
'''
*: 100 health
=: 10 health
-: 1 health

e.g. 57 health
57 // 10 # 5 =
57 %= 10 # 7
7 // 10 # 7 -
=====-------

e.g. 157 health
157 // 100 # 1 *
157 %= 100 # 57
57 // 10 # 5 =
57 %= 10 # 7
7 // 10 # 7 -

*=====-------

'''



def HealthBar(character):
    print(character.picture)
    tempHealth = character.health
    hundreds = tempHealth // 100
    tempHealth %= 100
    tens = tempHealth // 10
    ones = tempHealth % 10
    print(hundreds*"*"+tens*"="+ones*"-")
    

class PercyJackson(Role):
    def __init__(self, name):
        super().__init__(name)
        self.picture = "⚡️"
        self.attackpower = 20
        self.health = 200
        self.baseDefense = 100
        self.defense = 100
        self.attackStamina = 0.1
        self.defenseStamina = 0.2
#        mac_and_cheese
#        MacAndCheese
#        macAndCheese

class Elf(Role):
    def __init__(self, name):
        super().__init__(name)
        self.picture = "🧝"
        self.attackpower = 40
        self.health = 50
        self.baseDefense = 200
        self.defense = 200
        self.attackStamina = 0.2
        self.defenseStamina = 0.4

class Zelda(Role):
    def __init__(self,name):
        super().__init__(name)
        self.picture = "🗡"
        self.attackpower = 20
        self.health = 100
        self.baseDefense = 50
        self.defense = 50
        self.attackStamina = 0.15
        self.defenseStamina = 0.25

class NPC:
#enemy.health -= (Defense(enemy.defense)*self.attackpower)
    def attack(self,enemy):
        enemy.health -= self.attackpower
    
class GoodNPC(NPC):
    pass

class BadNPC(NPC):
    def __init__(self,name):
        global badNPCs, randint
        self.role = name
        if self.role == "NINJA":
            self.picture = "🥷"
            self.attackpower = 10
            self.health = 100
            self.defense = 50
        elif self.role == "OGRE":
            self.picture = "👹"
            self.attackpower = 10
            self.health = 500
            self.defense = 100
        elif self.role == "DEMON":
            self.picture = "👿"
            self.attackpower = 5
            self.health = 100
            self.defense = 20

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
        self.places = ("FRIDGE",)

        
        
    
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
        self.places = ("SAND", "CACTUS") # Fill this up



def displayHeroes():
    print("------")
    print("Heroes")
    print("------")
    for hero in heroes:
        print(hero)
    print()

def map():
    print("------")
    print("Places")
    print("------")
    for place in places:
        print(place)
    print()

def search(setting, role):
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
    if place == "SAND":
        Chances = randint(1,100)
        if 1 <= Chances <= 5:
            role.inventory["Sand Pail"]["Number"] += 1
            print("You got a Sand Pail!")
        else:
            role.inventory["Sand"]["Number"] += 1
            print("You got SAND!")
    elif place == "CACTUS":
        role.inventory["Cactus"]["Number"] += 1
        print("You found a cactus!")
    elif place == "CASTLE":
        Chances = randint(1,100)
        if 1 <= Chances <= 4:
            role.inventorty["Golden Log"] += 1
            print("SUPER RARE DROP: Golden Log!")
        else:
            role.inventory["Emerald"]["Number"] += 1
            print("You got an emerald.")
    elif place == "OCEAN":
        role.inventory["Gold"]["Number"] += 1
        print("You got gold!")
    elif place == "FRIDGE":
        role.inventory["Cookie"]["Number"] += 1
        print("You got a cookie!")
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
            search(setting,role)
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
                search(setting,role)
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
    while NumberDefeated < 10 or RoleHero.health <= 0:
        randnum = randint(1,100)
        start = 1
        end = 0
#        {"NINJA":0.05,"OGRE":0.01, "DEMON":0.94}
        for b in badNPCs:
            end += int(badNPCs[b]*100) #probability of spawning
            if start <= randnum <= end:
#               Fight!
                a = BadNPC(b)
                HealthBar(a)
                HealthBar(RoleHero)
                # Fight
                start = time()
                enemyMove = 1 if randint(1,2)==1 else 2
                enemyMoved = False
                ETTMA = random()/2 #Enemy Time To Move Again
                while RoleHero.health > 0 and a.health > 0:
                    try:
                        start = time()  # 100000000
                        TimeToMove = random()*3 # 4
                        move = inputimeout(prompt="1. to attack, 2. for temporary defense boost: ", timeout=TimeToMove)
                        while move != "1" and move != "2":
                            TimeToMove = TimeToMove + start - time()#100000004
                            if TimeToMove > 0:
                                move = inputimeout(prompt="1. to attack, 2. to defend: ", timeout=TimeToMove)
                            else:
                                raise TimeoutOccurred
#                        print(move)
#                        print(a.health)
                        if move=="1":
                            RoleHero.attack(a)
                        if move=="2":
                            RoleHero.defense += 250
                            print(RoleHero.defense)
                            RoleHero.defending = True
#                            RoleHero.health -= a.attackpower*Defense(RoleHero.defense)
#                            RoleHero.defense -= 250
                    except TimeoutOccurred:
                        a.attack(RoleHero)
                        if RoleHero.defending == True:
                            RoleHero.defense = RoleHero.baseDefense
                            RoleHero.defending = False
                        print(f"You were attacked! You have {RoleHero.health} remaining")
                            
                if RoleHero.health <= 0:
                    print("You are destroyed!")
                    return
                NumberDefeated+=1
                

            start=end+1
            
#            start=1
#            end=0
#            end=5
#            1 <= rn <= 5
#            start=6
#            end=6
#            6 <= rn <= 6
#            start=7
#            end=100
#            7 <= rn <= 100
            
            
    
    
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
    playerhero = (cS(input("What hero do you want to be? ")))
    while playerhero not in heroes:
        print("Error: Please try again")
        playerhero = (cS(input("What hero do you want to be? ")))
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