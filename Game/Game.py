from asyncio.events import BaseDefaultEventLoopPolicy
from string import punctuation, ascii_letters
from random import randint, choice, random
from time import time, sleep
from inputimeout import inputimeout, TimeoutOccurred
from threading import Thread
from tabulate import tabulate

Quests = False
Shop = False
# Roles
heroes = ("PERCY JACKSON", "ELF", "ZELDA")
goodNPCs = ("HEALER",)
badNPCs = {"NINJA": 0.05, "OGRE": 0.01, "DEMON": 0.94}
places = ("HOUSE", "BEACH", "FOREST", "MOUNTAIN", "DESERT")
neutralNPCs = ("MINER", "WOODCHUCKER")


def Defense(Def):
    return 1 - (Def / (Def + 100))


# Zeeshan Rizvi
# https://stackoverflow.com/questions/17432478/python-print-to-one-line-with-time-delay-between-prints/52595545#52595545?newreg=cb618a4b6ed14f8bb7a782e731f4c678
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


# A class is a user-defined type!!!


# Internet archive links
# https://web.archive.org
# Role Types
class Role:
    def __init__(self, name):
        self.name = name
        self.questLevel = 0

        '''
        Order of Magnitude = OM
        prob = probability

        OM
        __

        891

        8.91 * 10**2

        OM = 2

        1214

        1.214 * 10**3

        OM = 3

        971

        9.71 * 10**2

        OM = 2

        item                OM      prob

        cookie              2-3     .1-.01
        logs                3-4     .01-.001
        sands               0       10
        rocks               2       .1
        silvers             4       .001
        golds               5       .0001
        diamonds            7       .000001
        emeralds            7       .000001
        cactuses            3       .01
        golden saplings     8       .0000001
        golden logs         8       .0000001
        sand pails          5       .0001
        '''

        self.inventory = {
            # 1 "Cookies" = 1 cookie ≈ $4.25
            # 4.25/.0035 = 1214.2857142857142
            # https://bethebudget.com/how-much-to-charge-for-cookies/
            # https://web.archive.org/web/20220930045630/https://bethebudget.com/how-much-to-charge-for-cookies/
            "Cookies": {"Name": "Cookies", "Picture": "🍪", "Description": "Something to eat!", "Number": 0,
                        "BuyValue": 1214,
                        "SellValue": 971},

            # 1 "Logs" = 1 board = 10% of 1 log = $43.50
            # 43.50/.0035 = 12428.571428571428
            # https://markets.businessinsider.com/commodities/lumber-price
            # https://web.archive.org/web/20220930045534/https://markets.businessinsider.com/commodities/lumber-price
            "Logs": {"Name": "Logs", "Picture": "🪵",
                     "Description": "Something you can use in the shop for crafting things or to sell", "Number": 0,
                     "BuyValue": 12429, "SellValue": 9943},

            # Sand Cost in real life
            # 2000 pounds = $10.00
            # 1 Sands = 650 grams (1 handful)
            # 2000 pounds = 907184.7 grams
            # 1396 sands = $10.00
            # 1 sand = $0.007
            # 2 G = $0.007
            # 1 G = $0.0035 (= 2 yen as of September 17, 11:05 am PST)

            # sands : 1, gold : 751497

            #            Lesson on order of magnitude
            #            10**1 10**2 10**0 2e0 10e0
            #            100000 - 99999
            #            0 - 9.99 (repeating) e0

            "Sands": {"Name": "Sands", "Picture": "🟫", "Description": "Something you can smelt or sell!", "Number": 0,
                      "BuyValue": 2, "SellValue": 1},

            # Rock cost in real life
            # 2000 pounds = $30.00
            # 6 pounds = 1 handful = $0.9 = 90 257.14285714285717cents
            # .9/.0035 = 257.14285714285717

            "Rocks": {"Name": "Rocks", "Picture": "🪨",
                      "Description": "Something you can use in the shop for crafting things, selling, or refining",
                      "Number": 0, "BuyValue": 257, "SellValue": 206},

            # ONE ITEM OF SILVER = 1 pound bar = $302.08
            # 302.08/0.0035 = 86308.57142857142

            "Silvers": {"Name": "Iron Ore", "Picture": "🪙",
                        "Description": "Something you can use in the shop for crafting things, selling, or fusing",
                        "Number": 0, "BuyValue": 86309, "SellValue": 81993},

            # ONE ITEM OF GOLD = 1 pound bar = $26302.40
            # 26302.40/0.0035 = 751497.1428571428

            "Golds": {"Name": "Golds", "Picture": "⚱️",
                      "Description": "Something you can use in the shop for crafting things, selling, or fusing",
                      "Number": 0, "BuyValue": 751497, "SellValue": 747739},

            "Diamonds": {"Name": "Diamonds", "Picture": "💎",
                         "Description": "Something you can use in the shop for crafting things, selling, or fusing",
                         "Number": 0, "BuyValue": 42237143, "SellValue": 42143283},
            # 1 "Diamonds" = 5 carat diamond = $147,830
            # 147830/0.0035 = 42237142.85714286
            # https://www.diamondse.info/diamonds-price-index.asp
            # https://web.archive.org/web/20220930045549/https://www.diamondse.info/diamonds-price-index.asp

            "Emeralds": {"Name": "Emeralds", "Picture": "🟩",
                         "Description": "Something you can use in the shop for crafting things, selling, or fusing",
                         "Number": 0, "BuyValue": 35714286, "SellValue": 35674603},
            # 1 "Emerals" = 5 carat ≈ $125,000
            # 125000/.0035 = 35714285.71428572
            # https://emeralds.com/education/price-of-an-emerald/
            # https://web.archive.org/web/20220930045614/https://emeralds.com/education/price-of-an-emerald/

            # 1 "Cactuses" = 1 cheap cactus plant = $15
            # 15/.0035 = 4285.714285714285
            # https://www.gdncnursery.com/cactus
            # https://web.archive.org/web/20220930045627/https://www.gdncnursery.com/cactus
            "Cactuses": {"Name": "Cactuses", "Picture": "🌵",
                         "Description": "Something to sell or turn into pointy armour!",
                         "Number": 0, "BuyValue": 4286, "SellValue": 3429},

            # Game-only item, no real world equivalent, but ≈ $1,000,000
            # 1000000/.0035 = 285714285.71428573

            "Golden Saplings": {"Name": "Golden Saplings", "Picture": "🌸", "Description": "Grows into a golden tree!",
                                "Number": 0, "BuyValue": 285714286, "SellValue": 285685714},

            # Game-only item, no real world equivalent, but ≈ $500,000
            # 500000/.0035 = 142857142.85714287

            "Golden Logs": {"Name": "Golden Logs", "Picture": "🌴",
                            "Description": "The most powerful wood, when combined with weapons +10 to all stats!",
                            "Number": 0, "BuyValue": 142857143, "SellValue": 142851429},

            # Game-only item, no real world equivalent, but ≈ $400
            # 400/.0035 = 114285.71428571429

            "Sand Pails": {"Name": "Sand Pails", "Picture": "N/A",
                           "Description": "A bucket, maybe you can plant something in here.", "Number": 0,
                           "BuyValue": 114286, "SellValue": 108571},
            # sand pails = 20, vital for pregression
            "Keys": {
                "Key 1": {"Name": "Key 1", "Picture": "🔐", "Description": "Used to access a certain chest",
                          "Number": 0}}}

        # Big-O notation
        # Index a dictionary: O(1)
        # Search a dictionary: O(n)

        self.defending = False
        self.moved = False
        self.moveTime = None
        self.waitTime = None

    #    https://hypixel-skyblock.fandom.com/wiki/Defense
    def attack(self, enemy):
        #        enemy.health -= (Defense(enemy.defense)*self.attackpower)
        if not self.moved:
            self.moved = True
            enemy.health -= (Defense(enemy.defense) * self.attackpower)
            self.moveTime = time()
            self.waitTime = self.attackStamina
        elif time() - self.waitTime < self.moveTime:
            print("Can't attack yet")
        else:
            enemy.health -= (Defense(enemy.defense) * self.attackpower)
            self.moveTime = time()
            self.waitTime = self.attackStamina

    #            100 - ((1 - (50 / (50 + 100)))*10)

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
        temp = []  # temp is short for the word 'temporary'
        for item in self.inventory:
            if item == "Keys":
                for key in self.inventory["Keys"]:
                    if self.inventory["Keys"][key]["Number"] != 0:
                        print("{} {} {:>10}".format(self.inventory["Keys"][key]["Name"],
                                                    self.inventory["Keys"][key]["Picture"],
                                                    "x " + str(self.inventory["Keys"][key]["Number"])))
                        print("Description:", self.inventory["Keys"][key]["Description"])

            elif self.inventory[item]["Number"] != 0:
                temp.append((self.inventory[item]["Name"], self.inventory[item]["Picture"],
                             "x " + str(self.inventory[item]["Number"])))
        print()
        print(tabulate(temp, headers=("Name", "Picture", "Number")))
        print()

    #                print("{} {} {:>10}".format(self.inventory[item]["Name"],self.inventory[item]["Picture"],"x "+str(self.inventory[item]["Number"])))
    #                print("Description:",self.inventory[item]["Description"])

    def printSellItems(self):
        NoneConv = lambda x: 0 if x == None else x  # converts None/not None to 0/1
        temp = []  # temp is short for the word 'temporary'
        sellableItems = {}
        for item in self.inventory:
            if "SellValue" in self.inventory[item] and NoneConv(self.inventory[item].get("Number")) > 0:
                sellableItems[(self.inventory[item]["Name"]).upper()] = self.inventory[item]["Number"]

                temp.append((self.inventory[item]["Name"], self.inventory[item]["Picture"],
                             "x " + str(self.inventory[item]["Number"]), str(self.inventory[item]["SellValue"])))
        print()
        print(tabulate(temp, headers=("Item", "Picture", "Number", "Sell Value")))
        print()

        return sellableItems

    #        for item in self.inventory:
    #            if "SellValue" in self.inventory[item]:

    def baseLineStats(self):
        # health, defense, true health, money
        print()
        print(f"Attack Power = {self.attackpower}")
        print(f"Health = {self.health}")
        print(f"Defense = {self.baseDefense}")
        print(f"Attack Stamina = {self.attackStamina}")
        print(f"Defense Stamina = {self.defenseStamina}")
        print(f"Money = {self.money}")
        print()


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
    print(hundreds * "*" + tens * "=" + ones * "-")


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
        self.money = 50  # because the economy in italy is so bad :)


#    Naming variables convention
#        mac_and_cheese : snake case
#        MacAndCheese : pascal case
#        macAndCheese : camel case

class Elf(Role):
    def __init__(self, name):
        super().__init__(name)
        self.picture = "🧝"
        self.attackpower = 10
        self.health = 50
        self.baseDefense = 200
        self.defense = 200
        self.attackStamina = 2
        self.defenseStamina = 0.4
        self.money = 200


class Zelda(Role):
    def __init__(self, name):
        super().__init__(name)
        self.picture = "🗡"
        # TODO Change back to 20 for actual game
        self.attackpower = 2000
        self.health = 100
        self.baseDefense = 50
        self.defense = 50
        self.attackStamina = 0.15
        self.defenseStamina = 0.25
        self.money = 100


class NPC:
    # enemy.health -= (Defense(enemy.defense)*self.attackpower)
    def attack(self, enemy):
        #        enemy.health -= self.attackpower
        enemy.health -= (Defense(enemy.defense) * self.attackpower)


class GoodNPC(NPC):
    pass


class NeutralNPC(NPC):
    def __init__(self):
        global neutralNPCs, randint
        self.role = neutralNPCs[randint(0, len(neutralNPCs) - 1)]
        self.picture = "⛏" if self.role == "MINER" else "🪓"


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
        if cS(x) == "STOP":
            break
        stop = time()
        Time = (stop - start)
        print("You entered it in {:.2f} seconds!".format(Time))
        npcTime = 1 + (3 * random())

        if Time < npcTime and x == randletter:
            print("You passed!")
            wins += 1
            totalplayerscore += 1
            botavg.append(npcTime)
            playeravg.append(Time)
        elif Time > npcTime or x != randletter:
            print("You lost!")
            losses += 1
            totalplayerscore -= 1
            botavg.append(npcTime)
            playeravg.append(Time)
        elif Time == npcTime:
            print("Draw")
            draws += 1
            botavg.append(npcTime)
            playeravg.append(Time)
    playeravglen = (len(playeravg)) if len(playeravg) != 0 else 1
    playeravg = sum(playeravg)
    botavglen = (len(botavg)) if len(botavg) != 0 else 1
    botavg = sum(botavg)
    points = wins - losses
    if playeravg / playeravglen < botavg / botavglen:
        print("You get 5 extra resources because your avg was better than the bot!")
        points += 5

    if TheSetting == "BEACH":
        for i in range(points):
            role.inventory["Sands"]["Number"] += 1

    elif TheSetting == "FOREST":
        for i in range(points):
            Temprand = randint(1, 1000000)
            if 999999 <= Temprand <= 1000000:
                role.inventory["Golden Saplings"]["Number"] += 1
            if 999997 <= Temprand <= 999998:
                role.inventory["Golden Logs"]["Number"] += 1
            if 100000 <= Temprand <= 1000:
                role.inventory["Logs"]["Number"] += 1
            else:
                return
        return
    elif TheSetting == "HOUSE":
        for i in range(points):
            Temprand = randint(1, 100)
            if 1 <= Temprand <= 10:
                role.inventory["Cookies"]["Number"] += 1
            else:
                return
            return

    elif TheSetting == "MOUNTAIN":
        for i in range(points):
            Temprand = randint(1, 100000)
            if 1 <= Temprand <= 100:
                role.inventory["Silvers"]["Number"] += 1
            elif 2 <= Temprand <= 20:
                role.inventory["Golds"]["Number"] += 1
            elif 99999 <= Temprand <= 100000:
                role.inventory["Diamonds"]["Number"] += 1
            elif 99998 <= Temprand <= 99999:
                role.inventory["Emeralds"]["Number"] += 1
                #10000
            elif 3 <= Temprand <= 30000:
                role.inventory["Rocks"]["Number"] += 1
            else:
                return
            return
        return
    elif TheSetting == "DESERT":
        for i in range(points):
            Temprand = randint(1, 100)
            if 1 <= Temprand <= 2:
                role.inventory["Cactuses"]["Number"] += 1
            else:
                role.inventory["Sands"]["Number"] += 1

    print("The player average is {:.2f} seconds".format(playeravg / playeravglen))
    print("The bot average is {:.2f} seconds".format(botavg / botavglen))
    print("You got {} resources in total!".format(points))
    print("You won {} games!".format(wins))
    print("You lost {} games!".format(losses))
    print("{} is the number of games that drawed!".format(draws))

    return points


class BadNPC(NPC):
    def __init__(self, name):
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

    '''
    x   y
    -   --
    0   1
    1   1.2
    2   1.4
    3   1.6
    4   1.8
    5   2.0

    y = m*x+b

    m = 0.2
    b = 1

    x = 1:  y = 0.2*1+1 = 1.2
    x = 1.2: y = 0.2*1.2+1 = 1.24
    '''

    def statboost(self, RoleHero):
        multiplier = (0.2 * RoleHero.questLevel) + 1
        self.attackpower = multiplier * self.attackpower
        self.health = multiplier * self.health
        self.defense = multiplier * self.defense


# Setting Types
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
        self.places = ("SAND", "CASTLE", "OCEAN")  # Fill this up


class Forest(Setting):
    def __init__(self):
        self.name = "Forest"
        self.places = ("TREE",)  # Fill this up


class Mountain(Setting):
    def __init__(self):
        self.name = "Mountain"
        self.places = ("CAVE", "UP")  # Fill this up


class Desert(Setting):
    def __init__(self):
        self.name = "Desert"
        self.places = ("SAND", "CACTUS")  # Fill this up


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
        Chances = randint(1, 100)
        if 1 <= Chances <= 5:
            role.inventory["Sand Pails"]["Number"] += 1
            print("You got a Sand Pail!")
        else:

            role.inventory["Sands"]["Number"] += 1
            print("You got SAND!")
    elif place == "CACTUS":
        role.inventory["Cactuses"]["Number"] += 1
        print("You found a cactus!")
    elif place == "CASTLE":
        Chances = randint(1, 100)
        if 1 <= Chances <= 4:
            role.inventorty["Golden Logs"] += 1
            print("SUPER RARE DROP: Golden Log!")
        else:
            role.inventory["Emeralds"]["Number"] += 1
            print("You got an emerald.")
    elif place == "OCEAN":
        role.inventory["Golds"]["Number"] += 1
        print("You got gold!")
    elif place == "FRIDGE":
        role.inventory["Cookies"]["Number"] += 1
        print("You got a cookie!")
    return place


def HasSellableItems(inventory):
    for item in inventory:
        if item == "Keys":
            continue
        elif inventory[item]["Number"] > 0:
            return True
    return False


# User can buy or sell as many items as they wish, given that they have enough
# money
def shop(Role):
    inventory = Role.inventory  # alias
    while True:
        option = cS(input("Would you like to buy or sell today (type 'exit' to exit)? "))
        # Input validation
        while option != "BUY" and option != "SELL" and option != "EXIT":
            print("Try again!")
            option = cS(input("Would you like to buy or sell today? "))

        if option == "EXIT":
            return

        elif option == "BUY":
            if Role.money == 0:
                print("You don't have any money!")
                continue

            print(f"\nYour Money = {Role.money:0.2f}\n")
            BuyOption = cS(input("What would you like to buy today? "))


        elif option == "SELL":
            if not HasSellableItems(inventory):
                print("You don't have any sellable items!")
                continue

            sellableItems = Role.printSellItems()
            print(f"\nYour Money = {Role.money:0.2f}\n")
            SellOption = cS(input("What would you like to sell today? "))

            # Check if SellOption is a sellable item: Input validation
            while SellOption not in sellableItems:
                print(f"Error! {SellOption} is not one of your sellable items")
                SellOption = cS(input("What would you like to sell today? "))

            AmountToSell = input(f"How many {SellOption} would you like to sell? ")
            # short-circuit evaluation
            while not AmountToSell.isdigit() or int(AmountToSell) > sellableItems[SellOption]:
                # Note: not AmountToSell.isdigit() is being evaluated twice
                if not AmountToSell.isdigit():
                    print(f"Error! {AmountToSell} is not a valid digit! ")
                    AmountToSell = input(f"How many {SellOption} would you like to sell? ")
                elif int(AmountToSell) > sellableItems[SellOption]:
                    print(f"Error! You don't have {AmountToSell} {SellOption} to sell.")
                    AmountToSell = input(f"How many {SellOption} would you like to sell? ")
                    # Role.money
        ATS = int(AmountToSell)
        # Converting from all caps to first letter uppercase of each word
        # (rest lowercase)
        SellOption = SellOption.split()
        SellOption = " ".join([temp[0] + temp[1:].lower() for temp in SellOption])

        TTS = Role.inventory[SellOption]["SellValue"]
        Role.money = Role.money + ATS * TTS

        Role.inventory[SellOption]["Number"] -= ATS


#        for i in range(int(ATS)):
#            inventory - inventory[f"{SellOption}"]["Value"]

# Complete this part


def GetMenuOption():
    option = cS(input(
        "Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))
    while option not in ("MAP", "SEARCH", "QUESTS", "MINE", "INV", "SHOP", "STATS"):
        print("Try again!")
        option = cS(input(
            "Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))
    return option


def Menu(role, setting):
    # Only going to execute once
    if Quests == False:
        option = cS(input("Enter either 'Map' or 'Search' or 'Stats' "))
        # Input validation
        while option not in ("MAP", "SEARCH", "STATS"):
            print("Try again!")
            option = cS(input("Enter either 'Map' or 'Search'  or 'Stats' "))
        if option == "MAP":
            setting.map()
        elif option == "SEARCH":
            search(setting, role)
        elif option == "STATS":
            role.baseLineStats()

    # Will go on until user enters "Quests"
    elif Quests == True or Shop == True:
        '''
        Enter one of the following options
        ==================================

        '''
        option = cS(input(
            "Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))

        # Input validation
        while option not in ("MAP", "SEARCH", "QUESTS", "MINE", "INV", "SHOP", "STATS"):
            print("Try again!")
            option = cS(input(
                "Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))

        while option in ("MAP", "SEARCH", "MINE", "INV", "SHOP", "STATS"):
            if option == "MAP":
                setting.map()
                option = GetMenuOption()
            elif option == "SEARCH":
                search(setting, role)
                option = GetMenuOption()
            elif option == "STATS":
                role.baseLineStats()
                option = GetMenuOption()
            elif option == "MINE":
                Mine(role, setting)
                option = GetMenuOption()
            elif option == "INV":
                role.printInventory()
                option = GetMenuOption()
            elif option == "SHOP":
                if Shop == True:
                    shop(role)
                    option = GetMenuOption()
                else:
                    print("You do not have access to the shop yet!")
                    option = GetMenuOption()


def Quest1(RoleHero):
    # Implementing stacking, so they can only defend 10 times
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

    Stacks = [False] * 2

    def DefenseWait(index):
        sleep(5)
        if RoleHero.defense >= RoleHero.baseDefense + 250:
            RoleHero.defense -= 250
        # decrease the defense by one notch here
        Stacks[index] = False

    global badNPCs  # we're saying that we will be using the global variable badNPCs
    NumberDefeated = 0
    while NumberDefeated < 10 or RoleHero.health <= 0:
        randnum = randint(1, 100)
        start = 1
        end = 0
        #        {"NINJA":0.05,"OGRE":0.01, "DEMON":0.94}
        #
        for b in badNPCs:
            end += int(badNPCs[b] * 100)  # probability of spawning
            if start <= randnum <= end:
                # Fight!
                a = BadNPC(b)  # we are spawning an enemy here

                a.statboost(RoleHero)

                HealthBar(a)
                HealthBar(RoleHero)
                # Fight
                enemyMove = 1 if randint(1, 2) == 1 else 2
                enemyMoved = False
                ETTMA = random() / 2  # Enemy Time To Move Again
                while RoleHero.health > 0 and a.health > 0:
                    try:
                        start = time()  # 100000000
                        TimeToMove = random() * 3  # 4
                        if RoleHero.defending == True and start - RoleHero.moveTime > 0.1:
                            print("Defense Boost expired")
                            RoleHero.defending == False
                            RoleHero.defense = RoleHero.baseDefense

                        move = inputimeout(prompt="1. to attack, 2. for temporary defense boost: ", timeout=TimeToMove)
                        while move != "1" and move != "2":
                            TimeToMove = TimeToMove + start - time()  # 100000004
                            if TimeToMove > 0:
                                move = inputimeout(prompt="1. to attack, 2. for temporary defense boost: ",
                                                   timeout=TimeToMove)
                            else:
                                raise TimeoutOccurred
                        #                        print(move)
                        #                        print(a.health)
                        if move == "1":
                            RoleHero.attack(a)
                        if move == "2":

                            if all(Stacks):
                                print("You have reached your defense boost cap!")
                            else:
                                for stack in range(len(Stacks)):
                                    if Stacks[stack] == False:
                                        Stacks[stack] = True
                                        Thread(target=DefenseWait, args=(stack,)).start()
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
                NumberDefeated += 1

            start = end + 1
    print("You have completed the quest!")
    RoleHero.inventory["Keys"]["Key 1"]["Number"] = 1
    print("You now have access to the shop")
    RoleHero.questLevel += 1


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
        Menu(RoleHero, Place)
    elif placetogo == "BEACH":
        Place = Beach()
        Menu(RoleHero, Place)
    elif placetogo == "FOREST":
        Place = Forest()
        Menu(RoleHero, Place)
    elif placetogo == "MOUNTAIN":
        Place = Mountain()
        Menu(RoleHero, Place)
    elif placetogo == "DESERT":
        Place = Desert()
        Menu(RoleHero, Place)
    print("New thing unlocked! Quests have been unlocked.")
    global Quests, Shop
    Quests = True
    print("To open quests, in the menu quests will be unlocked.")
    Menu(RoleHero, Place)
    Quest1(RoleHero)
    Shop = True  # shop unlocked
    print("New thing unlocked! Shop has been unlocked.")
    Menu(RoleHero, Place)


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