from asyncio.events import BaseDefaultEventLoopPolicy
from string import punctuation, ascii_letters
from random import randint, choice, random
from time import time, sleep
from inputimeout import inputimeout, TimeoutOccurred
from threading import Thread

Quests = False
Shop = False
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


'''
cS is NOT an input function!!!

1. converts string to uppercase
2. gets rid of all of the punctuation
3. gets rid of leading and trailing spaces
'''

def cS(s):
    marksremoved = s.upper().translate(str.maketrans('', '', punctuation))
    return marksremoved.strip()

#Role Types
class Role:
    def __init__(self, name):
        self.name = name
        self.money = 100
        # Task 1: Modify descriptions of inventory
        self.inventory = {"Cookie":{"Name":"Cookie", "Picture":"🍪", "Description":"Something to eat!", "Number":0, "BuyValue":1, "SellValue":0},
        "Logs":{"Name":"Logs", "Picture":"🪵", "Description":"Something you can use in the shop for crafting things or to sell", "Number":0, "BuyValue": 5, "SellValue":4},
        "Sand":{"Name":"Sand", "Picture":"🟫", "Description":"Something you can smelt or sell!", "Number":0,"BuyValue":2, "SellValue":1},
        "Rocks":{"Name":"Rocks", "Picture":"🪨", "Description":"Something you can use in the shop for crafting things, selling, or refining", "Number":0, "BuyValue":5, "SellValue":4},
        "Silver":{"Name":"Silver", "Picture":"🪙", "Description":"Something you can use in the shop for crafting things, selling, or fusing","Number":0, "BuyValue": 20, "SellValue": 19},
        "Gold":{"Name":"Gold", "Picture":"⚱️", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0, "BuyValue": 200, "SellValue": 199},
        "Diamond":{"Name":"Diamond", "Picture":"💎", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0, "BuyValue":450, "SellValue":449},
        "Emerald":{"Name":"Emerald", "Picture":"🟩", "Description":"Something you can use in the shop for crafting things, selling, or fusing", "Number":0, "BuyValue":900,"SellValue":899},
        "Cactus":{"Name":"Cactus", "Picture":"🌵", "Description":"Something to sell or turn into pointy armour!", "Number":0, "BuyValue":5, "SellValue":4},
        "Golden Sapling":{"Name":"Golden Sapling", "Picture":"🌸", "Description":"Grows into a golden tree!", "Number":0, "BuyValue":50000, "SellValue": 49995},
        "Golden Log":{"Name":"Golden Log", "Picture":"🌴", "Description":"The most powerful wood, when combined with weapons +10 to all stats!", "Number":0, "BuyValue": 25000, "SellValue": 24999},
        "Sand Pail":{"Name":"Sand Pail", "Picture":"N/A","Description":"A bucket, maybe you can plant something in here.","Number":0, "BuyValue": 20, "SellValue": 19},
        "Sand":{"Name":"Sand", "Picture":"⌛","Description":"Sand, used for smelting into glass or for making sandpaper.","Number":0, "BuyValue": 1, "SellValue": 1}, "Keys":{"Key 1": {"Name":"Key 1", "Picture":"🔐","Description":"Used to access a certain chest","Number":0}}}
        
        self.defending = False
        self.moved = False
        self.moveTime = None
        self.waitTime = None

#    https://hypixel-skyblock.fandom.com/wiki/Defense
    def attack(self,enemy):
#        enemy.health -= (Defense(enemy.defense)*self.attackpower)
        if not self.moved:
            self.moved = True
            enemy.health -= (Defense(enemy.defense)*self.attackpower)
            self.moveTime = time()
            self.waitTime = self.attackStamina
        elif time() - self.waitTime < self.moveTime:
            print("Can't attack yet")
        else:
            enemy.health -= (Defense(enemy.defense)*self.attackpower)
            self.moveTime = time()
            self.waitTime = self.attackStamina
            
    def defend(self):
        if not self.moved:
            self.moved = True
            self.defending = True
            self.defense += 250
            self.moveTime = time()
            self.waitTime = self.defenseStamina
        elif time() - self.waitTime < self.moveTime:
            print("Can't boost defense yet")
        else:
            self.defense += 250
            self.moveTime = time()
            self.waitTime = self.defenseStamina
        
        print(self.defense)
#        self.defending = True
        
        
    def printInventory(self):
        for item in self.inventory:
            if self.inventory[item]["Number"] != 0:
                print("{} {} {:>10}".format(self.inventory[item]["Name"],self.inventory[item]["Picture"],"x "+str(self.inventory[item]["Number"])+self.inventory[item]["Key 1"], self.inventory[item]["Key 1"],"x "+str(self.inventory["Key 1"]["Number"])))
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
    tempHealth = int(character.health)
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
        self.attackStamina = 2
        self.defenseStamina = 0.4

class Zelda(Role):
    def __init__(self,name):
        super().__init__(name)
        self.picture = "🗡"
        self.attackpower = 2000 # Change back to 20 for actual game
        self.health = 100
        self.baseDefense = 50
        self.defense = 50
        self.attackStamina = 0.15
        self.defenseStamina = 0.25

class NPC:
#enemy.health -= (Defense(enemy.defense)*self.attackpower)
    def attack(self,enemy):
#        enemy.health -= self.attackpower
        enemy.health -= (Defense(enemy.defense)*self.attackpower)
            
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
    playeravglen = (len(playeravg)) if len(playeravg)!=0 else 1
    playeravg = sum(playeravg)
    botavglen = (len(botavg)) if len(botavg)!=0 else 1
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

# User can buy or sell as many items as they wish, given that they have enough
# money
def shop(Role):
    inventory = self.inventory # alias
    option = cS(input("Would you like to buy or sell today (type 'exit' to exit)? "))
    # Input validation
    while option != "BUY" and option != "SELL" and option != "EXIT":
        print("Try again!")
        option = cS(input("Would you like to buy or sell today? "))
    
    if option == "EXIT":
        return
    
    elif option == "BUY":
        BuyOption = cS(input("What would you like to buy today? "))
    elif option == "SELL":
        SellOption = cS(input("What would you like to sell today? "))
    

def GetMenuOption():
    option = cS(input("Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n\n"))
    while option not in ("MAP","SEARCH","QUESTS", "MINE", "INV", "SHOP"):
        print("Try again!")
        option = cS(input("Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n\n"))
    return option

def Menu(role, setting):
    # Only going to execute once
    if Quests == False:
        option = cS(input("Enter either 'Map' or 'Search' "))
        # Input validation
        while option not in ("MAP","SEARCH"):
            print("Try again!")
            option = cS(input("Enter either 'Map' or 'Search' "))
        if option == "MAP":
            setting.map()
        elif option == "SEARCH":
            search(setting,role)
            
    # Will go on until user enters "Quests"
    elif Quests == True or Shop == True:
        '''
        Enter one of the following options
        ==================================
        
        '''
        option = cS(input("Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n\n"))
        
        #Input validation
        while option not in ("MAP","SEARCH","QUESTS", "MINE", "INV", "SHOP"):
            print("Try again!")
            option = cS(input("Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n\n"))
        
        
        while option in ("MAP","SEARCH","QUESTS", "MINE", "INV", "SHOP"):
            if option == "MAP":
                setting.map()
                option = GetMenuOption()
            elif option == "SEARCH":
                search(setting,role)
                option = GetMenuOption()
            elif option == "MINE":
                Mine(role,setting)
                option = GetMenuOption()
            elif option == "INV":
                role.printInventory()
                option = GetMenuOption()
            elif option == "SHOP":
                if Shop == True:
                    shop(role)
                    option = GetMenuOption()
            elif option == "QUESTS":
                if Quests == True:
                    Quest1(RoleHero)
                else:
                    print("You do not have access to the shop yet!")
                    option = GetMenuOption()

def Quest1(RoleHero):
    #Implementing stacking, so they can only defend 10 times
#    Stack1 = False
#    Stack2 = False
#    Stack3 = False
#    Stack4 = False
#    Stack5 = False
#    Stack6 = False
#    Stack7 = False
#    Stack8 = False
#    Stack9 = False
#    Stack10 = False

        

    Stacks = [False]*2
    
    def DefenseWait(index):
        sleep(5)
        if RoleHero.defense >= RoleHero.baseDefense + 250:
            RoleHero.defense -= 250
        #decrease the defense by one notch here
        Stacks[index] = False
        
    global badNPCs # we're saying that we will be using the global variable badNPCs
    NumberDefeated = 0
    while NumberDefeated < 10 or RoleHero.health <= 0:
        randnum = randint(1,100)
        start = 1
        end = 0
#        {"NINJA":0.05,"OGRE":0.01, "DEMON":0.94}1
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
                        if RoleHero.defending == True and start - RoleHero.moveTime > 0.1:
                            print("Defense Boost expired")
                            RoleHero.defending == False
                            RoleHero.defense = RoleHero.baseDefense
                            
                        move = inputimeout(prompt="1. to attack, 2. for temporary defense boost: ", timeout=TimeToMove)
                        while move != "1" and move != "2":
                            TimeToMove = TimeToMove + start - time()#100000004
                            if TimeToMove > 0:
                                move = inputimeout(prompt="1. to attack, 2. for temporary defense boost: ", timeout=TimeToMove)
                            else:
                                raise TimeoutOccurred
#                        print(move)
#                        print(a.health)
                        if move=="1":
                            RoleHero.attack(a)
                        if move=="2":
                        
                            if all(Stacks):
                                print("You have reached your defense boost cap!")
                            else:
                                for stack in range(len(Stacks)):
                                    if Stacks[stack] == False:
                                        Stacks[stack] = True
                                        Thread(target=DefenseWait,args = (stack,)).start()
                                        break
                                RoleHero.defend()
                            
            
                    except TimeoutOccurred:
                        start = time()
                        if RoleHero.defending == True and start - RoleHero.moveTime > 0.1:
                            print("Defense Boost expired")
                            RoleHero.defending == False
                            RoleHero.defense = RoleHero.baseDefense
                            
                        
                        a.attack(RoleHero)
                        if RoleHero.defending == True:
                            RoleHero.defense = RoleHero.baseDefense
                            RoleHero.defending = False
                        print(f"You were attacked! You have {RoleHero.health:.2f} remaining")

                            
                if RoleHero.health <= 0:
                    print("You are destroyed!")
                    return
                NumberDefeated+=1
                

            start=end+1
    print("You have completed the quest!")
    print("You now have access to the shop")
            
            
#
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
    global Quests, Shop
    Quests = True
    print("To open quests, in the menu quests will be unlocked.")
    Menu(RoleHero,Place)
    Quest1(RoleHero)
    Shop = True
    Menu(RoleHero,Place)
    
    
def game():
    slowPrint("Welcome to the Game!")
#    Animation
    displayHeroes()
    playerhero = (cS(input("What hero do you want to be? ")))
    while playerhero not in heroes:
        print("Error: Please try again")
        playerhero = (cS(input("What hero do you want to be? ")))
    HeroGame(playerhero)
game()