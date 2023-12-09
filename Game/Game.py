from asyncio.events import BaseDefaultEventLoopPolicy
from string import punctuation, ascii_letters
from random import randint, choice, random
from time import time, sleep
from inputimeout import inputimeout, TimeoutOccurred
from threading import Thread
from tabulate import tabulate
import cppyy
import pygame
from io import BytesIO
import requests
from PIL import Image
import os
import numpy as np
from collections import deque

Quests = False
Shop = False
# Roles
heroes = ("PERCY JACKSON", "ELF", "ZELDA")
goodNPCs = ("HEALER",)
places = ("HOUSE", "BEACH", "FOREST", "MOUNTAIN", "DESERT")
neutralNPCs = ("MINER", "WOODCHUCKER")


def Defense(Def):
    return 1 - (Def / (Def + 100))


# TODO:
#####
# Implement buy function of def shop -> possibly add some items ✅
# Add use function for each of the items
# Boost stats of hero after a quest, and maybe also after mining? ✅
# quest2 -> In C programming
# Work on menu option function where you can use some of your items to build weapons that can boost your stats 👨‍💻
# figure out use case of items not attainable through mining
# implement a save function
# saving => writes information to a file (e.g. time, stats, items, time that the RoleHero last searched etc.)
# modify search option so that it can only occur once per people day ✅
# Axes that can increase drop-chances for mine function
# Find out where we can increase money besides selling

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
    return ''.join(c for c in s if c not in punctuation).upper().strip()


# A class is a user-defined type!!!

# Internet archive links
# https://web.archive.org
# Role Types
cppyy.cppdef(
    r'''
    double Defense(double Def)
    {
        return 1 - (Def / (Def + 100));
    }
    //'Time Since Epoch In Millisecs'
    uint64_t time()
    {
        using namespace std::chrono;
        return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
    }

    std::unordered_map<std::string, double> badNPCs = {{"NINJA", 0.33} , {"OGRE", 0.33} , {"DEMON", 0.34}};

    struct Role;

    struct BadNPC
    {
        const std::string name;
        std::string picture;
        double attackpower;
        double health;
        double defense;
        double expYield;
        double speed;
        double attackStamina;
        bool moved;
        bool flipped;
        uint64_t moveTime;
        uint64_t waitTime;

        BadNPC(const std::string& Name);

        void attack(Role&);
        void statboost(Role&);
        void update_wait_time();
        bool can_attack();
    };

    BadNPC::BadNPC(const std::string& Name) : name{Name}, moved{false}, moveTime{0}, waitTime{0}, flipped{false}
    {
        if (name == "NINJA") //second most powerful
        {
            this->picture = "🥷";
            this->attackpower = 7;
            this->health = 100.0;
            this->defense = 50;
            this->expYield = 10;
            this->speed = 1.5;
            this->attackStamina = 0.7;

        }
        else if (name == "OGRE") //most powerful
        {
            this->picture = "👹";
            this->attackpower = 15;
            this->health = 500.0;
            this->defense = 100;
            this->expYield = 25;
            this->speed = 1;
            this->attackStamina = 0.9;
        }
        else if (name == "DEMON") //least powerful
        {
            this->picture = "👿";
            this->attackpower = 10;
            this->health = 100.0;
            this->defense = 20;
            this->expYield = 5;
            this->speed = 1.25;
            this->attackStamina = 0.9;
        }
    }


    struct Role
    {
        std::string name;
        int questLevel;
        double searchtime;
        bool defending;
        bool moved;
        bool flipped;
        uint64_t moveTime;
        uint64_t waitTime;

        std::unordered_map<std::string, std::unordered_map<std::string,std::string>> stringInv;
        std::unordered_map<std::string, std::unordered_map<std::string,double>> numInv;
        std::unordered_map<std::string,std::unordered_map<std::string,std::function<void()>>> useInv;

        double health;
        double basehealth;
        double attackpower;
        double defense;
        double attackStamina;
        double defenseStamina;
        double money;
        double baseDefense;
        double searchTime;
        int maxLevel;
        int startLevel;
        int currLevel;
        double currExp;
        double LevelExp;
        double speed;
    //    virtual double ExpLevelFunc(double){}
        bool can_attack();
        void update_wait_time();
        void defend();
        void attack(BadNPC& enemy);
        void baseLineStats();
        std::vector<std::string> printInventory();
        std::unordered_map<std::string, double> printSellItems(bool print = false);
        std::vector<std::string> printSellItemsVec(bool print = false, bool upper = true);
        std::vector<std::string> getTradableItems();
        std::unordered_map<std::string, double> printBuyItems();
        std::pair<std::unordered_map<std::string, std::unordered_map<std::string, double>>, std::vector<std::string>> printTradeInfo();
        double AttackLevelFunc(int level)
        {
            return 20*pow((1-0.05),level);
        }
        double HealthLevelFunc(int level)
        {
            return 40.233 - 9.60068*pow(level,0.300144);
        }
        double DefenseLevelFunc(int level)
        {
            return 100.583 - 24.0017*pow(level,0.300144);
        }
        double StaminaLevelFunc(int level)
        {
            return exp(-1*(level+1));
        }
        double SpeedLevelFunc(int level)
        {
            return ((level < 4) ? exp(-0.6*level) : 0.091);
        }

    //    virtual void increaseExp(double exp); //Declaration

        Role(std::string name);
        virtual ~Role();
    };

    void BadNPC::attack(Role& RoleHero)
    {
        RoleHero.health -= (Defense(RoleHero.defense) * attackpower);
    }

    void Role::defend() //:: is the scope resolution operator
    {
        if (!moved)
        {
            moved = true;
            defending = true;
            defense += 250;
            moveTime = time();
            waitTime = static_cast<uint64_t>(defenseStamina*1000);
        }
        else if (time() - waitTime < moveTime)
        {
            std::cout << "Can't boost defense yet\n";
        }
        else
        {
            defense += 250;
            moveTime = time();
            waitTime = static_cast<uint64_t>(defenseStamina*1000);
        }
    }

    //false
    //not moved? (only first time)
    //true
    //Enemy health = (some value)

    //The current has to be at least 'waitTime' further in the future than when the role last attacked 'moveTime'
    bool Role::can_attack()
    {
        return ((!moved) || (time() - waitTime >= moveTime));
    }

    //The current BadNPC has to be at least 'waitTime' further in the future than when the BadNPC last attacked 'moveTime'
    bool BadNPC::can_attack()
    {
        return ((!moved) || (time() - waitTime >= moveTime));
    }

    void Role::update_wait_time()
    {
        if (!moved)
        {
            moved = true;
        }
        moveTime = time();
        waitTime = static_cast<uint64_t>(attackStamina*1000);
    }

    void BadNPC::update_wait_time()
    {
        if (!moved)
        {
            moved = true;
        }
        moveTime = time();
        waitTime = static_cast<uint64_t>(attackStamina*1000);
    }

    void Role::attack(BadNPC& enemy)
    {
        enemy.health -= (Defense(enemy.defense) * attackpower);
    }

    void Role::baseLineStats()
    {
        std::cout << "\nAttack Power = " << std::setprecision(0)
        << std::fixed << attackpower << '\n'
        << "Health = " << std::setprecision(0)
        << std::fixed << health << " / " << std::setprecision(0)
        << std::fixed << basehealth << '\n'
        << "Defense = " << std::setprecision(0)
        << std::fixed << defense << " / " << std::setprecision(0)
        << std::fixed << baseDefense << '\n'
        << "Attack Stamina = " << attackStamina << '\n'
        << "Defense Stamina = " << defenseStamina << '\n'
        << "Money = " << money << '\n'
        << "Quest Level = " << questLevel << '\n'
        << "Stat Level = " << currLevel << '\n'
        << "Exp = " << std::setprecision(2)
        << std::fixed << currExp << " / " << std::setprecision(2)
        << std::fixed << LevelExp
        << "\n\n";
    }

    //scaling the BadNPCs stats depending on the Quest#; higher the quest, stronger the BadNPC's
    void BadNPC::statboost(Role& RoleHero)
    {
        double multiplier = (0.2 * RoleHero.questLevel) + 1;
        attackpower = multiplier * attackpower;
        health = multiplier * health;
        defense = multiplier * defense;
        expYield = multiplier * expYield;
        speed = multiplier * speed;
        //TODO: divide stamina by multiplier
    }

    std::vector<std::string> Role::printInventory()
    {
        std::vector<std::string> currentInventory;

        std::cout << std::setw(15) << "Name" << std::setw(15) << "Picture" << std::setw(15) << "Number" << '\n' << std::setw(15) << "----" << std::setw(15) << "-------" << std::setw(15) << "------" << '\n';

        for (auto& i: stringInv)
        {
    //            "Name", "Picture", "Number"
            if (numInv[i.first]["Number"] > 0)
            {
                std::cout << std::setw(15) << stringInv[i.first]["Name"] << std::setw(15) << stringInv[i.first]["Picture"] << std::setw(15) << numInv[i.first]["Number"] << '\n';

                std::string temp = i.first;
                std::transform(temp.begin(), temp.end(),temp.begin(), ::toupper);
                currentInventory.push_back(temp);
            }
        }
        std::cout << '\n';
        return currentInventory;
    }
    //print = true, prints out AND returns map
    //print = false, ONLY returns map, doesn't print anything
    std::unordered_map<std::string, double> Role::printSellItems(bool print)
    {

        if (print)
        {
            std::cout << std::setw(15) << "Item" << std::setw(15) << "Picture" << std::setw(15) << "Number" <<
            std::setw(15) << "Sell Value" << '\n' << std::setw(15) << "----" << std::setw(15) << "-------" << std::setw(15) << "------" << std::setw(15) << "----------" << '\n';
        }

        std::unordered_map<std::string, double> sellableItems;
        for (auto& i: stringInv)
        {
    //            "Item", "Picture", "Number", "Sell Value"
            if ((numInv[i.first].find("SellValue") != numInv[i.first].end()) && (numInv[i.first]["Number"] > 0))
            {
                if (print)
                {
                    std::cout << std::setw(15) << stringInv[i.first]["Name"] << std::setw(15) << stringInv[i.first]["Picture"] << std::setw(15) << numInv[i.first]["Number"] << std::setw(15) << numInv[i.first]["SellValue"] << '\n';
                }
                std::string temp = i.first;
                std::transform(temp.begin(), temp.end(), temp.begin(), ::toupper);
                sellableItems[temp] = numInv[i.first]["Number"];
            }
        }
        return sellableItems;
    }

    //print = true, prints out AND returns map
    //print = false, ONLY returns map, doesn't print anything
    std::vector<std::string> Role::printSellItemsVec(bool print, bool upper)
    {
        if (print)
        {
            std::cout << std::setw(15) << "Item" << std::setw(15) << "Picture" << std::setw(15) << "Number" <<
            std::setw(15) << "Sell Value" << '\n' << std::setw(15) << "----" << std::setw(15) << "-------" << std::setw(15) << "------" << std::setw(15) << "----------" << '\n';
        }

        std::vector<std::string> sellableItems;
        for (auto& i: stringInv)
        {
    //            "Item", "Picture", "Number", "Sell Value"
            if ((numInv[i.first].find("SellValue") != numInv[i.first].end()) && (numInv[i.first]["Number"] > 0))
            {
                if (print)
                {
                    std::cout << std::setw(15) << stringInv[i.first]["Name"] << std::setw(15) << stringInv[i.first]["Picture"] << std::setw(15) << numInv[i.first]["Number"] << std::setw(15) << numInv[i.first]["SellValue"] << '\n';
                }
                std::string temp = i.first;
                //Turning everything to uppercases
                if (upper)
                {
                    std::transform(temp.begin(), temp.end(), temp.begin(), ::toupper);
                }
                sellableItems.push_back(temp);
            }
        }
        return sellableItems;

    }

    std::vector<std::string> Role::getTradableItems()
    {
        std::vector<std::string> tradableItems;
        for (auto& i: stringInv)
        {
            if (stringInv[i.first].count("Construction") && (numInv[i.first]["Questlevel"] <= this->questLevel)) //if found
            {
                tradableItems.push_back(i.first);
            }
        }
        return tradableItems;
    }

    std::unordered_map<std::string, double> Role::printBuyItems()
    {
        std::unordered_map<std::string, double> buyableItems;

        std::cout << std::setw(20) << "Item" << std::setw(20) << "Picture" <<
                std::setw(20) << "Buy Value" << '\n' << std::setw(20) << "----" << std::setw(20) << "-------" << std::setw(20) << "---------" << '\n';

        for (auto& i: stringInv)
        {
        //            "Item", "Picture", "Buy Value"
            if ((numInv[i.first].find("BuyValue") != numInv[i.first].end()) && (numInv[i.first]["Questlevel"] <= this->questLevel))
            {
                std::cout << std::setw(20) << stringInv[i.first]["Name"] << std::setw(20) << stringInv[i.first]["Picture"] << std::setw(20) << numInv[i.first]["BuyValue"] << std::setw(20) << '\n';
                std::string temp = i.first;
                std::transform(temp.begin(), temp.end(),temp.begin(), ::toupper);
                buyableItems[temp] = numInv[i.first]["BuyValue"];
            }
        }
        std::cout << '\n';
        return buyableItems;
    }

    std::unordered_map<std::string, double> TradeItemDict(const std::string& construction)
    {
        std::stringstream ss;
        std::string temp;
        // std::vector<std::string> tokens;
        std::unordered_map<std::string, double> dict;

        ss << construction;

        while (getline(ss, temp, ','))
        {
            // tokens.push_back(temp);
            // std::cout << temp << '\n';
            size_t last_index = temp.find_last_of("0123456789");
            int num = std::stoi(temp.substr(0, last_index+1));

            last_index = temp.find_last_of(" ");
            dict[temp.substr(last_index+1)] = num;
        }

        return dict;
    }

    std::pair<std::unordered_map<std::string, std::unordered_map<std::string, double>>, std::vector<std::string>> Role::printTradeInfo()
    {
        //false, false, means don't print sell items (just return the vector
        //of sell items, and don't make the sellitems all uppercase)
        std::vector<std::string> sellInfo = printSellItemsVec(false, false);

        //get's the items that we can trade for
        std::vector<std::string> tradableItems = getTradableItems();
        auto tradeSize = tradableItems.size();
        auto sellSize = sellInfo.size();
        std::unordered_map<std::string, std::unordered_map<std::string, double>> tradeInfo;
        std::unordered_map<std::string, double> dict;
        int i = 0;

        int maxTradeLength = 0;
        int maxSellLength = 0;

        if (tradeSize > sellSize)
        {
            //calculate lengths
            for (auto& k: tradableItems)
            {
                int tempTradeLength = 0, tempSellLength = 0; //temporaries

                //calculate tempSellLength
                if (i < sellSize)
                {
                    tempSellLength = sellInfo[i].length() + stringInv[sellInfo[i]]["Picture"].length() + std::to_string(numInv[sellInfo[i]]["Number"]).length() + 5;

    //                tempSellLength = sellInfo[i].length() + 1 + std::to_string(numInv[sellInfo[i]]["Number"]).length() + 5;

                    if (maxSellLength < tempSellLength)
                    {
                        maxSellLength = tempSellLength; //update the max sell length
                    }

                    i++;
                }

                dict = TradeItemDict(stringInv[k]["Construction"]);
                tradeInfo[k] = dict;
                tradeInfo[k]["Money"] = static_cast<int>(numInv[k]["BuyValue"]);

                tempTradeLength =  k.length() + 2 + stringInv[k]["Picture"].length();
    //            tempTradeLength = k.length() + 2 + 1;

                for (auto& j: dict)
                {
                    tempTradeLength += 5 + stringInv[j.first]["Picture"].length() + std::to_string(static_cast<int>(j.second)).length();
    //                tempTradeLength += 5 + 1 + std::to_string(static_cast<int>(j.second)).length();
                }

                tempTradeLength += 5 + std::to_string(numInv[k]["BuyValue"]).length();

                if (maxTradeLength < tempTradeLength)
                {
                    maxTradeLength = tempTradeLength; //update the max trade length
                }
            }
            i = 0;
            std::cout << maxTradeLength << '\n';
            //output stuff using calculated lengths
            for (auto& k: tradableItems)
            {
                std::string temp;
                if (i < sellSize)
                {
                    int numInvVal = static_cast<int>(numInv[sellInfo[i]]["Number"]);
                    std::string numInvString = std::to_string(numInvVal);

                    temp = sellInfo[i] + ": " + stringInv[sellInfo[i]]["Picture"] + " x " + numInvString;

                    std::cout << std::setw(maxSellLength) << temp;
                    i++;
                }
                else
                {
                    std::cout << std::setw(maxSellLength) << "";
                }
                std::cout << "          ";
                //Output the trade items
                dict = TradeItemDict(stringInv[k]["Construction"]);

                temp = k + ' ' + stringInv[k]["Picture"] + ':';

                for (auto& j: dict)
                {
                    temp += ' ' + stringInv[j.first]["Picture"] + " x " + std::to_string(static_cast<int>(j.second)) + ',';
                }

                double numInvVal = numInv[k]["BuyValue"];
                std::string numInvString = std::to_string(numInvVal);

                temp += " $ = " + numInvString.substr(0, numInvString.find(".")+3);
                std::cout << std::setw(maxTradeLength) << temp;
                std::cout << '\n';
            }

            return std::make_pair(tradeInfo,sellInfo);
        }

    //    User Inventory                      Stuff you can trade for
    //    ==============                      =======================
    //    Sands: 🟫 x 1                       Armor 🛡️: 🪨 x 20, ..., $ = 142857

    //    When the user has more sellable items than the # of
    //    items currently available for trading

        //calculate  lengths
        for (auto& k: sellInfo)
        {
            int tempTradeLength = 0, tempSellLength = 0; //temporaries

            tempSellLength = k.length() + 5 + stringInv[k]["Picture"].length() + std::to_string(numInv[k]["Number"]).length();

            if (tempSellLength > maxSellLength)
            {
                maxSellLength = tempSellLength;
            }

            if (i < tradeSize)
            {
                dict = TradeItemDict(stringInv[tradableItems[i]]["Construction"]);
                tradeInfo[tradableItems[i]] = dict;
                tradeInfo[tradableItems[i]]["Money"] = static_cast<int>(numInv[tradableItems[i]]["BuyValue"]);

                tempTradeLength = tradableItems[i].length() + 2 + stringInv[tradableItems[i]]["Picture"].length();

                for (auto& j: dict)
                {
                    tempTradeLength += 5 + stringInv[j.first]["Picture"].length() + std::to_string(static_cast<int>(j.second)).length();
                }

                tempTradeLength += 5 + std::to_string(numInv[tradableItems[i]]["BuyValue"]).length();
                i++;
            }
        }

        i = 0;
        //output the stuff
        for (auto& k: sellInfo)
        {
            int numInvVal = static_cast<int>(numInv[k]["Number"]);
            std::string numInvString = std::to_string(numInvVal);

            std::string temp = k + ": " +
            stringInv[k]["Picture"] + " x " +
            numInvString;

            std::cout << std::setw(maxSellLength) << temp;

            if (i < tradeSize)
            {
                std::cout << "          ";
                dict = TradeItemDict(stringInv[tradableItems[i]]["Construction"]);

                temp = tradableItems[i] + ' ' + stringInv[tradableItems[i]]["Picture"] + ':';

                for (auto& j: dict)
                {
                    temp += ' ' + stringInv[j.first]["Picture"] + " x " + std::to_string(static_cast<int>(j.second)) + ',';
                }

                double numInvVal = numInv[tradableItems[i]]["BuyValue"];
                std::string numInvString = std::to_string(numInvVal);

                temp += " $ = " + numInvString.substr(0, numInvString.find(".")+3);

                std::cout << std::setw(maxTradeLength) << temp;
                i++;
            }
            std::cout << '\n';
        }

        return std::make_pair(tradeInfo,sellInfo);
    }

    Role::Role(std::string name)
    {
        this->name = name;
        questLevel = 0;
        searchtime = 0;
        defending = false;
        moved = false;
        flipped = false;
        moveTime = 0;
        waitTime = 0;
        health = 0;
        basehealth = 0;
        attackpower = 0;
        defense = 0;
        attackStamina = 0;
        defenseStamina = 0;
        money = 0;
        searchTime = 0;
        maxLevel = 100;
        startLevel = 1; //start at the minimum level
        currLevel = startLevel;
        currExp = 0;
        LevelExp = 0; //override in derived classes
        speed = 0;

    //        for (auto i : stringInv)
    //        for i in stringInv

        stringInv =
        {
                {
                        "Cookies",{{"Name", "Cookies"}, {"Picture", "Assets/cookie.png"}, {"Description", "Something to eat! Increase health by 10% "}, {"Type", "Healing"}}
                },

                {
                        "Logs",{{"Name", "Logs"}, {"Picture", "Assets/log.png"}, {"Description", "Something you can use in the shop for crafting things or to sell "}, {"Type", "Misc"}}
                },

                {
                        "Sands",{{"Name", "Sands"}, {"Picture", "Assets/sand.png"}, {"Description", "Something you can smelt or sell! "}, {"Type", "Misc"}}
                },

                {
                        "Rocks",{{"Name", "Rocks"}, {"Picture", "Assets/rock.png"}, {"Description", "Something you can use in the shop for crafting things, selling, or refining "}, {"Type", "Misc"}}
                },

                {
                        "Silvers",{{"Name", "Iron Ore"}, {"Picture", "Assets/silver.png"}, {"Description", "Something you can use in the shop for crafting things, selling, or fusing "}, {"Type", "Misc"}}
                },

                {
                        "Golds",{{"Name", "Golds"}, {"Picture", "Assets/gold.png"}, {"Description", "Something you can use in the shop for crafting things, selling, or fusing "}, {"Type", "Misc"}}
                },

                {
                        "Diamonds",{{"Name", "Diamonds"}, {"Picture", "Assets/diamond.png"}, {"Description", "Something you can use in the shop for crafting things, selling, or fusing "}, {"Type", "Misc"}}
                },

                {
                        "Emeralds",{{"Name", "Emeralds"}, {"Picture", "Assets/emerald.png"}, {"Description", "Something you can use in the shop for crafting things, selling, or fusing "}, {"Type", "Misc"}}
                },

                {
                        "Cactuses",{{"Name", "Cactuses"}, {"Picture", "Assets/cactus.png"}, {"Description", "Something to sell or turn into pointy armour! "}, {"Type", "Misc"}}
                },

                {
                        "Golden Saplings",{{"Name", "Golden Saplings"}, {"Picture", "Assets/sapling.png"}, {"Description", "Grows into a golden tree! "}, {"Type", "Misc"}}
                },

                {
                        "Golden Logs",{{"Name", "Golden Logs"}, {"Picture", "Assets/Golden Log.png"}, {"Description", "The most powerful wood, when combined with weapons +10 to all stats! "}, {"Type", "Misc"}}
                },

                {
                        "Sand Pails",{{"Name", "Sand Pails"}, {"Picture", "Assets/Sand Pail.png"}, {"Description", "A bucket, maybe you can plant something in here! "}, {"Type", "Misc"}}
                },

                {
                        "Potion",{{"Name", "Potion"}, {"Picture", "Assets/Assets/potion.png"}, {"Description", "A potion, maybe you can drink it (Increases health by 20)"}, {"Type", "Healing"}}
                },

                {
                        "Apple",{{"Name", "Apple"}, {"Picture", "Assets/apple.png"}, {"Description", "An apple, maybe you can eat it(Increases health by 10)! "}, {"Type", "Healing"}}
                },

                {
                        "Key 1",{{"Name", "Key 1"}, {"Picture", "Assets/key.png"}, {"Description", "A key, maybe you can use it to open something! "}, {"Type", "Key"}}
                },

                {
                        "Knife",{{"Name", "Knife"}, {"Picture", "Assets/knife.png"}, {"Description", "A knife, maybe you can use it to attack enemies! "}, {"Type", "Weapon"}, {"Construction", "5 Rocks, 2 Logs, 1 Silvers"}}
                },

                {
                        "Parrot",{{"Name", "Parrot"}, {"Picture", "Assets/parrot.png"}, {"Description", "A parrot, does passive damage to enemies! "}, {"Type", "Misc"}, {"Construction", "5 Apple, 3 Logs, 1 Potion"}}
                },

                {
                        "Ring",{{"Name", "Ring"}, {"Picture", "Assets/ring.png"}, {"Description", "A ring, increases your stats! "}, {"Type", "Misc"}, {"Construction", "5 Diamonds, 3 Golds, 1 Silvers"}}
                },

                {
                        "Cape",{{"Name", "Cape"}, {"Picture", "Assets/cape.png"}, {"Description", "A cape, increases your stats! "}, {"Type", "Misc"}, {"Construction", "5 Emeralds, 20 Sands"}}
                },

                {
                        "Armor",{{"Name", "Armor"}, {"Picture", "Assets/armour.png"}, {"Description", "Armor, increases your stats! "}, {"Type", "Misc"}, {"Construction", "20 Rocks"}}
                },

                {
                        "Water Guns",{{"Name", "Water Guns"}, {"Picture", "Assets/water gun.png"}, {"Description", "Water Gun, maybe you can use it to attack enemies! "}, {"Type", "Misc"}, {"Construction", "1 Sands, 1 Potion"}}
                }
        };

        numInv =
        {
                {
                        "Cookies",{{"Number", 0}, {"BuyValue", 1214}, {"SellValue", 971}, {"Questlevel", 1}}
                },

                {
                        "Logs",{{"Number", 0}, {"BuyValue", 12429}, {"SellValue", 9943}, {"Questlevel", 1}}
                },

                {
                        "Sands",{{"Number", 0}, {"BuyValue", 2}, {"SellValue", 1}, {"Questlevel", 1}}
                },

                {
                        "Rocks",{{"Number", 0}, {"BuyValue", 256}, {"SellValue", 206}, {"Questlevel", 1}}
                },

                {
                        "Silvers",{{"Number", 0}, {"BuyValue", 86309}, {"SellValue", 81993}, {"Questlevel", 4}}
                },

                {
                        "Golds",{{"Number", 0}, {"BuyValue", 751497}, {"SellValue", 747739}, {"Questlevel", 6}}
                },

                {
                        "Diamonds",{{"Number", 0}, {"BuyValue", 42237143}, {"SellValue", 42143283}, {"Questlevel", 8}}
                },

                {
                        "Emeralds",{{"Number", 0}, {"BuyValue", 35714286}, {"SellValue", 35674603}, {"Questlevel", 10}}
                },

                {
                        "Cactuses",{{"Number", 0}, {"BuyValue", 4286}, {"SellValue", 3429}, {"Questlevel", 1}}
                },

                {
                        "Golden Saplings",{{"Number", 0}, {"BuyValue", 285714286}, {"SellValue", 285685714}, {"Questlevel", 1}}
                },

                {
                        "Golden Logs",{{"Number", 0}, {"BuyValue", 142857143}, {"SellValue", 142851429}, {"Questlevel", 1}}
                },

                {
                        "Sand Pails",{{"Number", 0}, {"BuyValue", 114286}, {"SellValue", 108571}, {"Questlevel", 1}}
                },

                {
                        "Potion",{{"Number", 0}, {"BuyValue", 26}, {"SellValue", 13}, {"Questlevel", 1}}
                },

                {
                        "Apple",{{"Number", 0}, {"BuyValue", 1214}, {"SellValue", 971}, {"Questlevel", 1}}
                },

                {
                        "Key 1",{{"Number", 0}, {"Questlevel", 1}}
                },

                {
                        "Knife",{{"Number", 0}, {"BuyValue", 2876}, {"Questlevel", 2}} //2
                },

                {
                        "Parrot",{{"Number", 0}, {"BuyValue", 7468}, {"Questlevel", 4}} //4
                },

                {
                        "Ring",{{"Number", 0}, {"BuyValue", 9765}, {"Questlevel", 4}} //4
                },

                {
                        "Cape",{{"Number", 0}, {"BuyValue", 6541}, {"Questlevel", 7}} //7
                },

                {
                        "Armor",{{"Number", 0}, {"BuyValue", 142857}, {"Questlevel", 7}} //7
                },

                {
                        "Water Guns",{{"Number", 0}, {"BuyValue", 100}, {"Questlevel", 1}} //7
                },

        };

        useInv =
        {
            {
                "Cookies",{{"Use",
                                   [&]()
                                   {
                                       health += 0.1*health;
                                       if (health > basehealth)
                                       {
                                           health = basehealth;
                                       }
                                       if (numInv["Cookies"]["Number"] > 0)
                                       {
                                           numInv["Cookies"]["Number"]--;
                                       }
                                   }
                           }}
            },

            {
                "Logs",{{"Use",
                                   [&]()
                                   {
                                       if (numInv["Logs"]["Number"] > 0)
                                       {
                                           numInv["Logs"]["Number"]--;
                                       }
                                       return;
                                   }
                           }}
            },

            {
                "Key 1",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Key 1"]["Number"] > 0)
                                        {
                                            numInv["Key 1"]["Number"]--;
                                        }
                                        return;
                                   }
                           }}
            },

            {
                "Sands",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Sands"]["Number"] > 0)
                                        {
                                            numInv["Sands"]["Number"]--;
                                        }
                                        return;
                                   }
                           }}
            },

            {
                "Rocks",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Rocks"]["Number"] > 0)
                                        {
                                            numInv["Rocks"]["Number"]--;
                                        }
                                        return;
                                   }
                           }}
            },

            {
                "Silvers",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Silvers"]["Number"] > 0)
                                        {
                                            numInv["Silvers"]["Number"]--;
                                        }
                                       return;
                                   }
                           }}
            },

            {
                "Golds",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Golds"]["Number"] > 0)
                                        {
                                            numInv["Golds"]["Number"]--;
                                        }
                                       return;
                                   }
                           }}
            },

            {
                "Diamonds",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Diamonds"]["Number"] > 0)
                                        {
                                            numInv["Diamonds"]["Number"]--;
                                        }
                                       return;
                                   }
                           }}
            },

            {
                "Emeralds",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Emeralds"]["Number"] > 0)
                                        {
                                            numInv["Emeralds"]["Number"]--;
                                        }
                                        return;
                                   }
                           }}
            },

            {
                "Cactuses",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Cactuses"]["Number"] > 0)
                                        {
                                            numInv["Cactuses"]["Number"]--;
                                        }
                                       return;
                                   }
                           }}
            },

            {
                "Golden Saplings",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Golden Saplings"]["Number"] > 0)
                                        {
                                            numInv["Golden Saplings"]["Number"]--;
                                        }
                                       return;
                                   }
                           }}
            },

            {
                "Golden Logs",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Golden Logs"]["Number"] > 0)
                                        {
                                            numInv["Golden Logs"]["Number"]--;
                                        }
                                        return;
                                   }
                           }}
            },

            {
                "Sand Pails",{{"Use",
                                   [&]()
                                   {
                                        if (numInv["Sand Pails"]["Number"] > 0)
                                        {
                                            numInv["Sand Pails"]["Number"]--;
                                        }
                                        return;
                                   }
                           }}
            },

            {
                "Potion",{{"Use",
                                   [&]()
                                   {
                                       health += 20;
                                       if (this->health > basehealth)
                                       {
                                           health = basehealth;
                                       }
                                       if (numInv["Potion"]["Number"] > 0)
                                       {
                                            numInv["Potion"]["Number"]--;
                                       }
                                   }
                           }}
            },

            {
                "Apple",{{"Use",
                                   [&]()
                                   {
                                       health += 0.25*health;
                                       if (this->health > basehealth)
                                       {
                                           health = basehealth;
                                       }
                                       if (numInv["Apple"]["Number"] > 0)
                                       {
                                            numInv["Apple"]["Number"]--;
                                       }
                                   }
                           }}
            },

            {
                "Knife",{{"Use",
                                    [&]()
                                    {
                                        if (numInv["Knife"]["Number"] > 0)
                                        {
                                            numInv["Knife"]["Number"]--;
                                        }
                                        return;
                                    }
                        }}
            },

            {
                "Parrot",{{"Use",
                                    [&]()
                                    {
                                        if (numInv["Parrot"]["Number"] > 0)
                                        {
                                            numInv["Parrot"]["Number"]--;
                                        }
                                        return;
                                    }
                        }}
            },

            {
                "Ring",{{"Use",
                                    [&]()
                                    {
                                        if (numInv["Ring"]["Number"] > 0)
                                        {
                                            numInv["Ring"]["Number"]--;
                                        }
                                        return;
                                    }
                        }}
            },

            {
                "Cape",{{"Use",
                                    [&]()
                                    {
                                        if (numInv["Cape"]["Number"] > 0)
                                        {
                                            numInv["Cape"]["Number"]--;
                                        }
                                        return;
                                    }
                        }}
            },

            {
                "Armor",{{"Use",
                                    [&]()
                                    {
                                        if (numInv["Armor"]["Number"] > 0)
                                        {
                                            numInv["Armor"]["Number"]--;
                                        }
                                        return;
                                    }
                        }}
            },

            {
                "Water Guns",{{"Use",
                                    [&]()
                                    {
                                        if (numInv["Water Guns"]["Number"] > 0)
                                        {
                                            numInv["Water Guns"]["Number"]--;
                                        }
                                        return;
                                    }
                        }}
            }
        };
    }

    Role::~Role()
    {
        //empty
    }

    //void Role::increaseExp(double exp) //Definition
    //{
    //    currExp += netExp;
    //    while (currExp > LevelExp)
    //    {
    //        currLevel++; // Increase the level of the role
    //        netExp = currExp - LevelExp;
    //        LevelExp = ExpLevelFunc(currLevel + 1);
    //        currExp = 0;
    //        currExp += netExp;
    //    }
    //}

    bool HasSellableItems(std::unordered_map<std::string, std::unordered_map<std::string,double>>& inventory)
    {
        for (auto &i : inventory)
        {
            if ((i.second.find("SellValue") != i.second.end()) && i.second["Number"] > 0)
            {
                return true;
            }
        }

        return false;
    }
''')
from cppyy.gbl import Role, BadNPC, badNPCs, HasSellableItems


# Takes in a C++ string, and returns a correct python string
def cppStringConvert(string):
    temp = ""
    for i in range(string.length()):
        temp = temp + string[i]
    return temp  # a python string


class PercyJackson(Role):
    def __init__(self, name):
        super().__init__(name)
        self.picture = "⚡️"
        self.attackpower = 20
        self.basehealth = 200
        self.health = 200
        self.baseDefense = 100
        self.defense = 100
        self.attackStamina = 0.1
        self.defenseStamina = 0.2
        self.speed = 0.3
        self.ExpLevelFunc = lambda x: x ** 2.5
        self.LevelExp = self.ExpLevelFunc(self.currLevel + 1)
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
        self.basehealth = 50
        self.health = 50
        self.baseDefense = 200
        self.defense = 200
        self.attackStamina = 0.2
        self.defenseStamina = 0.4
        self.speed = 0.1
        self.ExpLevelFunc = lambda x: x ** 1.5
        self.LevelExp = self.ExpLevelFunc(self.currLevel + 1)
        self.money = 200


class Zelda(Role):
    def __init__(self, name):
        super().__init__(name)
        self.picture = "🗡"
        # TODO: Change back to 20 for actual game
        self.attackpower = 2000
        self.basehealth = 100
        self.health = 100
        self.baseDefense = 50
        self.defense = 50
        self.attackStamina = 0.15
        self.defenseStamina = 0.25
        self.speed = 0.3
        self.ExpLevelFunc = lambda x: x ** 2
        #        https://www.thoughtco.com/calculate-decay-factor-2312218
        #        self.AttackLevelFunc = lambda x: 20*(1-0.05)**x
        self.LevelExp = self.ExpLevelFunc(self.currLevel + 1)
        self.money = 100


class NeutralNPC:
    def __init__(self):
        global neutralNPCs, randint
        self.role = neutralNPCs[randint(0, len(neutralNPCs) - 1)]
        if self.role == "MINER":
            self.picture = "⛏"
            self.expYield = 0.1 + random() / 20  # random number from 0.1 - 0.15
        elif self.role == "WOODCHUCKER":
            self.picture = "🪓"
            self.expYield = 0.12 + random() / 50  # random number from 0.12 - 0.14


def increaseStats(role):
    role.attackpower += role.AttackLevelFunc(role.currLevel)
    role.basehealth += role.HealthLevelFunc(role.currLevel)
    role.health += role.HealthLevelFunc(role.currLevel)
    role.baseDefense += role.DefenseLevelFunc(role.currLevel)
    role.attackStamina -= role.StaminaLevelFunc(role.currLevel)
    role.defenseStamina -= role.StaminaLevelFunc(role.currLevel)
    role.defense = role.baseDefense
    role.speed += role.SpeedLevelFunc(role.currLevel)


def increaseExp(role, netExp):
    role.currExp += netExp
    while role.currExp > role.LevelExp:
        role.currLevel += 1  # Increase the level of the role
        increaseStats(role)
        netExp = role.currExp - role.LevelExp
        role.LevelExp = role.ExpLevelFunc(role.currLevel + 1)
        role.currExp = 0
        role.currExp += netExp


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
        elif Time == npcTime:  # Probably never happen
            print("Draw")
            draws += 1
            botavg.append(npcTime)
            playeravg.append(Time)
    playeravglen = (len(playeravg)) if len(playeravg) != 0 else 1
    playeravg = sum(playeravg)
    botavglen = (len(botavg)) if len(botavg) != 0 else 1
    botavg = sum(botavg)
    points = wins - losses

    netExp = points * Opponent.expYield if points >= 0 else 0

    #    role.currExp += netExp
    #    while role.currExp > role.LevelExp:
    #        role.currLevel += 1 #Increase the level of the role
    #        netExp = role.currExp - role.LevelExp
    #        role.LevelExp = role.ExpLevelFunc(role.currLevel+1)
    #        role.currExp = 0
    #        role.currExp += netExp

    increaseExp(role, netExp)

    if playeravg / playeravglen < botavg / botavglen:
        print(f"You get 5 extra resources because your avg was better than the {Opponent.role} {Opponent.picture}!")
        points += 5

    #        cookie              2-3     1-.1
    #        logs                3-4     .1-.01
    #        sands               0       100
    #        rocks               2       1
    #        silvers             4       .01
    #        golds               5       .001
    #        diamonds            7       .00001
    #        emeralds            7       .00001
    #        cactuses            3       .1
    #        golden saplings     8       .000001
    #        golden logs         8       .000001
    #        sand pails          5       .001

    if TheSetting == "BEACH":
        role.numInv["Sands"]["Number"] += points

    #    3 <= x <= 5 #x is between 3 and 5 inclusive
    #    3 < x < 5 #x is between 3 and 5 exclusive
    elif TheSetting == "FOREST":
        for i in range(points):
            Temprand = randint(1, 1e8)
            if Temprand == 1e8:
                role.numInv["Golden Saplings"]["Number"] += 1
            elif Temprand == 1:
                role.numInv["Golden Logs"]["Number"] += 1
            elif 10000 <= Temprand <= 100000:
                role.numInv["Logs"]["Number"] += 1

    elif TheSetting == "HOUSE":
        for i in range(points):
            Temprand = randint(1, 1000)
            if 1 <= Temprand <= 5:
                role.numInv["Cookies"]["Number"] += 1

    elif TheSetting == "MOUNTAIN":
        for i in range(points):
            Temprand = randint(1, 1e7)
            if 1 <= Temprand <= 1000:
                role.numInv["Silvers"]["Number"] += 1
            elif 1001 <= Temprand <= 1100:
                role.numInv["Golds"]["Number"] += 1
            elif Temprand == 1101:
                role.numInv["Diamonds"]["Number"] += 1
            elif Temprand == 1102:
                role.numInv["Emeralds"]["Number"] += 1
                # 10000
            elif 1103 <= Temprand <= 101102:
                role.numInv["Rocks"]["Number"] += 1

    elif TheSetting == "DESERT":
        role.numInv["Sands"]["Number"] += points
        for i in range(points):
            Temprand = randint(1, 1000)
            if Temprand == 1:
                role.numInv["Cactuses"]["Number"] += 1

    print("The player average is {:.2f} seconds".format(playeravg / playeravglen))
    print("The {} {} average is {:.2f} seconds".format(Opponent.role, Opponent.picture, botavg / botavglen))
    print("You got {} resources in total!".format(points))
    print("You won {} games!".format(wins))
    print("You lost {} games!".format(losses))
    print("{} is the number of games that drawed!".format(draws))

    return points


def displayHeroes(printing=False):
    lines = ["------", "Heroes", "------"]
    for hero in heroes:
        lines.append(hero)
    lines.append("")
    print("\n".join(lines)) if not printing else print()
    return lines


# User can buy or sell as many items as they wish, given that they have enough
# money
def shop(Role):
    #    inventory = Role.inventory  # alias
    while True:
        print("What would you like to do today? (Type 'exit' to exit)")
        print("======================================================")
        print("Buy\nSell\nTrade\n")
        option = cS(input())
        # Input validation
        while option != "BUY" and option != "SELL" and option != "EXIT" and option != "TRADE":
            print("Try again!")
            option = cS(input("Enter either 'buy', 'sell', 'trade' or 'exit': "))

        if option == "EXIT":
            return

        elif option == "BUY":
            if Role.money == 0:
                print("You don't have any money!")
                continue

            '''
            print out the items that have the QuestLevel key

            buyableItems = Role.printBuyItems()
            '''

            print(f"\nYour Money = {Role.money:0.2f}\n")
            buyableItems = Role.printBuyItems()
            BuyOption = cS(input("What would you like to buy today? "))

            while buyableItems.find(BuyOption) == buyableItems.end():
                print(f"Error! {BuyOption} is not one of your buyable items")
                BuyOption = cS(input("What would you like to buy today? "))
            AmountToBuy = input(f"How many {BuyOption} would you like to buy? ")
            while not AmountToBuy.isdigit() or int(AmountToBuy) * buyableItems[BuyOption] > Role.money:
                # Note: not AmountToSell.isdigit() is being evaluated twice
                if not AmountToBuy.isdigit():
                    print(f"Error! {AmountToBuy} is not a valid digit! ")
                    AmountToBuy = input(f"How many {BuyOption} would you like to buy? ")
                elif int(AmountToBuy) * buyableItems[BuyOption] > Role.money:
                    print(f"Error! You don't have enough money to buy {AmountToBuy} {BuyOption}")
                    AmountToBuy = input(f"How many {BuyOption} would you like to buy? ")
            ATB = int(AmountToBuy)
            # Converting from all caps to first letter uppercase of each word
            # (rest lowercase)
            BuyOption = DictKeyFormatter(BuyOption.split())

            TTS = Role.numInv[BuyOption]["BuyValue"]
            Role.money = Role.money - ATB * TTS

            Role.numInv[BuyOption]["Number"] += ATB

        elif option == "SELL":
            if not HasSellableItems(Role.numInv):
                print("You don't have any sellable items!")
                continue

            sellableItems = Role.printSellItems(True)
            print(f"\nYour Money = {Role.money:0.2f}\n")
            SellOption = cS(input("What would you like to sell today? "))

            # Check if SellOption is a sellable item: Input validation
            while sellableItems.find(SellOption) == sellableItems.end():
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
            SellOption = DictKeyFormatter(SellOption.split())

            TTS = Role.numInv[SellOption].at("SellValue")
            Role.money = Role.money + ATS * TTS

            # SyntaxError: 'function call' is an illegal expression for augmented assignment
            #            Role.numInv[SellOption].at("Number")
            Role.numInv[SellOption]["Number"] -= ATS

        elif option == "TRADE":
            if not HasSellableItems(Role.numInv):
                print("You don't have any tradable items!")
                continue
            Info = Role.printTradeInfo()
            TradeInfo = Info.first
            SellInfo = Info.second

            print(f"\nYour Money = {Role.money:0.2f}\n")
            TradeOption = cS(input("What would you like to trade for today? ")).title()

            while TradeInfo.find(TradeOption) == TradeInfo.end():
                print(f"Error! {TradeOption} is not one of the tradeable items.")
                TradeOption = cS(input("What would you like to trade for today? ")).title()

            RequiredTradeItems = TradeInfo[TradeOption]

            TradeFor(Role, SellInfo, RequiredTradeItems, TradeOption)


#            TODO: Create a boolean function that takes WhatToTradeFor, and SellInfo, and returns true if it can be traded for and false otherwise.

#
#        1. Figure out if the item the user enters is a tradeable item
#            -> A list of the tradeable items
#        2. How many of said tradeable item the user wants to trade for
#            -> Input validation, as before
#        3. Check if the user has enough money and the necessary items to trade for x number of said item.
#            -> Calculate how much x of said items cost
#            -> See if user has enough money
#            -> See if user has enough items to trade for x of said items
#
#
#        Things we need
#        ==============
#        1. A list of sellable items: vector<string>
#        2. unordered_map<string, unordered_map<string, double>> ✅


#            User Inventory                      Stuff you can trade for
#            ==============                      =======================
#            Sands: 🟫 x 1                       Armor 🛡️: 🪨 x 20, ..., $ = 142857

def GetMenuOption():
    option = cS(input(
        "Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))
    while option not in ("MAP", "SEARCH", "QUESTS", "MINE", "INV", "SHOP", "STATS"):
        print("Try again!")
        option = cS(input(
            "Enter one of the following options\n=================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))
    return option


def ProcessInvRequest(role):
    currentInventory = role.printInventory()
    if not currentInventory:  # checking if it's empty
        print("Empty Inventory!\n")
        return
    option = cS(input("Select one of the above items: "))
    #    print(*[j+"\n" if i > 0 else " "+j+"\n"  for i, j in enumerate(currentInventory)])
    while option not in currentInventory:
        print("Select one of the following items\n=================================")
        currentInventory = role.printInventory()
        option = cS(input())
    todo = cS(input("Enter either 'description' for a description of the item, or 'use' to use the item: "))
    # Entry controlled loop
    options = ("DESCRIPTION", "USE")
    while todo not in options:
        print("Try again!")
        todo = cS(input("Enter either 'description' for a description of the item, or 'use' to use the item: "))

    option = option.split()
    if todo == "DESCRIPTION":
        print()
        print(role.stringInv[DictKeyFormatter(option)]["Description"])
        print()
    elif todo == "USE":
        print()
        role.useInv[DictKeyFormatter(option)]["Use"]()
        print()


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


#################################################################################################

pygame.init()
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
light_pink = (255, 182, 193)
orange = (255, 165, 0)
X = 800
Y = 750
screen = pygame.display.set_mode((X, Y))
font = pygame.font.Font('freesansbold.ttf', 32)


def pygame_print(text, loc=Y // 2, color=black, background_color=white, offset=0):
    text = font.render(text, True, color, background_color)
    textRect = text.get_rect()
    textRect.center = (X // 2 + offset, loc)
    screen.blit(text, textRect)
    return textRect


def updateList(items: list, selectNumber: int, color: tuple = light_pink, inc: int = 40, height: float = 4,
               new_screen=True) -> None:
    count = 0
    screen.fill(color) if new_screen else True
    for num, item in enumerate(items):
        pygame_print(item, Y // height + count, color=(yellow if num == selectNumber else black),
                     background_color=color)
        pygame.display.update()
        count += inc


# all images are in Game/Game/Assets
def displayImage(rsp, height: bool = False, p: int = 0, update: bool = True):
    global screen
    rsp = os.getcwd() + "/Assets/" + rsp
    pilimage = Image.open(rsp).convert("RGBA")
    if p == 0:
        pilimage = pilimage.resize((350, 350))
    elif p == 1:
        pilimage = pilimage.resize((800, 750))
    pgimg = pygame.image.fromstring(pilimage.tobytes(), pilimage.size, pilimage.mode)
    if not height:
        height = (125 - pgimg.get_rect().height) / 8

    screen.fill(white)
    screen.blit(pgimg, ((X - pgimg.get_rect().width) // 2, height))
    if update:
        pygame.display.update()


def openChestOption(optionNumber=None):
    pygame_print("Yes", Y // 1.5 + 60,
                 color=(orange if optionNumber == 0 else black)) if optionNumber == 0 else pygame_print("Yes",
                                                                                                        Y // 1.5 + 60,
                                                                                                        color=black)
    pygame_print("No", Y // 1.5 + 100, color=(orange if optionNumber == 1 else black))
    pygame.display.update()


def PlaceOption(optionNumber=None):
    pygame_print("House", 150, color=(orange if optionNumber == 0 else black))
    pygame_print("Beach", 190, color=(orange if optionNumber == 1 else black))
    pygame_print("Forest", 230, color=(orange if optionNumber == 2 else black))
    pygame_print("Mountain", 270, color=(orange if optionNumber == 3 else black))
    pygame_print("Desert", 310, color=(orange if optionNumber == 4 else black))
    pygame.display.update()


# Setting Types
class Setting:
    def map(self):
        global font, white, black

        screen.fill(white)
        pygame_print("--------", 90)
        pygame_print("Places", 130)
        pygame_print("--------", 170)

        currHeight = 210
        font = pygame.font.Font('freesansbold.ttf', 28)
        for place in self.places:
            pygame_print(place.title(), currHeight)
            currHeight += 40
        font = pygame.font.Font('freesansbold.ttf', 32)
        pygame.display.update()
        while True:
            for event in pygame.event.get():  # update the option number if necessary
                if event.type == pygame.KEYDOWN:  # checking if any key was selected
                    if event.key == pygame.K_RETURN:
                        print("exiting menu")
                        return


class House(Setting):
    def __init__(self):
        self.name = "House"
        self.places = ("FRIDGE",)


class Beach(Setting):
    def __init__(self):
        self.name = "Beach"
        self.places = ("SANDBAR", "CASTLE", "OCEAN")  # Fill this up


class Forest(Setting):
    def __init__(self):
        self.name = "Forest"
        self.places = ("TREE",)  # Fill this up


class Mountain(Setting):
    def __init__(self):
        self.name = "Mountain"
        self.places = ("CAVE", "TOP")  # Fill this up


class Desert(Setting):
    def __init__(self):
        self.name = "Desert"
        self.places = ("LANDSCAPE", "HILLSIDE")  # Fill this up


def search(setting, role):
    currentTime = time()
    if currentTime - role.searchTime < 86400:
        screen.fill(white)
        time_til_search = (86400 - (currentTime - role.searchTime)) / 60
        message = f"Sorry, you cannot search at this point! Time until you can search again = {time_til_search:.2f} minutes"
        temp = ""
        count = 0
        #        print(message)
        length = len(message)
        for i in range(length):
            temp += message[i]
            # displaying a new line every 24 characters
            if ((i + 1) % 24 == 0 and i != 0) or (i == length - 1):
                pygame_print(temp, 90 + count)
                temp = ""
                count += 50

        pygame.display.update()
        pygame.time.delay(1000)
        pygame.event.clear(eventtype=pygame.KEYDOWN)
        return

    optionNumber = 0
    numOptions = len(setting.places)
    breakFlag = False
    while True:
        screen.fill(white)  # clear the screen

        currHeight = 90
        Question = f"Where in the {setting.name} do you want to explore?"
        pygame_print(Question[0:Question.index("do") - 1], currHeight)
        currHeight += 40
        pygame_print(Question[Question.index("do"):], currHeight)
        currHeight += 60
        pygame_print("------", currHeight)
        currHeight += 40
        pygame_print("Places", currHeight)
        currHeight += 40
        pygame_print("------", currHeight)

        currHeight += 40
        currentOption = 0
        for place in setting.places:
            pygame_print(place.title(), currHeight, orange) if optionNumber == currentOption else pygame_print(
                place.title(), currHeight)
            currHeight += 40
            currentOption += 1
        pygame_print("------", currHeight)
        pygame.display.update()

        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != numOptions - 1 else 0
                elif event.key == pygame.K_UP:
                    optionNumber = optionNumber - 1 if optionNumber != 0 else numOptions - 1
                elif event.key == pygame.K_RETURN:
                    print(setting.places[optionNumber])
                    # TODO: Finish search function images to display
                    screen.fill(white)  # clear the screen
                    breakFlag = True  # enables breaking out of while-loop
                    break  # Breaking out of the pygame for-loop

        if breakFlag:
            break  # break out of while-loop here

    #        item                OM      prob (percentage out of 100)
    #
    #
    #        cookie              2-3     1-.1
    #        logs                3-4     .1-.01
    #        sands               0       100
    #        rocks               2       1
    #        silvers             4       .01
    #        golds               5       .001
    #        diamonds            7       .00001
    #        emeralds            7       .00001
    #        cactuses            3       .1
    #        golden saplings     8       .000001
    #        golden logs         8       .000001
    #        sand pails          5       .001

    # The user will have chosen a place to search at this point, so now we just run it
    # through all the possible places, and see if they get lucky

    if setting.places[optionNumber] == "SANDBAR":
        Chances = randint(1, 100000)
        role.numInv["Sands"]["Number"] += 1
        pygame_print("You got SAND!", 200)
        displayImage("sand.png", p=0)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second
        if Chances == 1:
            role.numInv["Sand Pails"]["Number"] += 1
            screen.fill(white)  # clear the screen
            pygame_print("You got a Sand Pail!", 200)
            displayImage("sand-pail.png", p=0)
            pygame.display.update()
            pygame.time.delay(1000)  # waiting one second

    elif setting.places[optionNumber] == "HILLSIDE":
        Chances = randint(1, 1000)
        role.numInv["Sands"]["Number"] += 1
        pygame_print("You got SAND!", 200)
        displayImage("hillside.png", p=0)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second
        if Chances == 1:
            role.numInv["Cactuses"]["Number"] += 1
            screen.fill(white)  # clear the screen
            pygame_print("You found a cactus!", 200)
            displayImage("cactus.png", p=0)
            pygame.display.update()
            pygame.time.delay(1000)  # waiting one second

    elif setting.places[optionNumber] == "CASTLE":
        Chances = randint(1, 1e8)
        if Chances == 1:
            role.numInv["Golden Logs"] += 1
            pygame_print("SUPER RARE DROP: Golden Log!", 200)
            displayImage("Golden log.png", p=0)
        elif 2 <= Chances <= 11:
            role.numInv["Emeralds"]["Number"] += 1
            displayImage("emerald.png", p=0)
            pygame_print("You got an emerald.", 200)
        else:
            pygame_print("Nothing found.", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second

    elif setting.places[optionNumber] == "OCEAN":
        Chances = randint(1, 1e5)
        if Chances == 1:
            role.numInv["Golds"]["Number"] += 1
            displayImage("gold.png", p=0)
            pygame_print("You got gold!", 200)
        else:
            pygame_print("Nothing found.", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second

    elif setting.places[optionNumber] == "FRIDGE":
        Chances = randint(1, 1000)
        if 1 <= Chances <= 5:
            role.numInv["Cookies"]["Number"] += 1
            displayImage("cookie.png", p=0)
            pygame_print("You got a cookie!", 200)
        else:
            pygame_print("Nothing found.", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second

    elif setting.places[optionNumber] == "TREE":
        Chances = randint(1, 1000)
        if 1 <= Chances <= 5:
            role.numInv["Apple"]["Number"] += 1
            displayImage("apple.png", p=0)
            pygame_print("You got an apple!", 200)
        else:
            pygame_print("Nothing found.", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second

    elif setting.places[optionNumber] == "CAVE":
        Chances = randint(1, 10000)
        if Chances == 1:
            role.numInv["Silvers"]["Number"] += 1
            displayImage("silver.png", p=0)
            pygame_print("You got a piece of silver!", 200)
        elif 2 <= Chances <= 101:
            role.numInv["Rocks"]["Number"] += 1
            displayImage("rock.png", p=0)
            pygame_print("You got a rock!", 200)
        else:
            pygame_print("Nothing found.", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second

    #    100000/10 = 10000 -> 1e5/10 = 1e4
    #   1/100 = 10/1000 = 100/10000 = 1000/100000
    elif setting.places[optionNumber] == "TOP":
        Chances = randint(1, 1e5)
        if Chances == 1:
            role.numInv["Golds"]["Number"] += 1
            displayImage("gold.png", p=0)
            pygame_print("You got a piece of gold!", 200)
        elif 2 <= Chances <= 11:
            role.numInv["Silvers"]["Number"] += 1
            displayImage("silver.png", p=0)
            pygame_print("You got a piece of silver!", 200)

        elif 12 <= Chances <= 1011:
            role.numInv["Rocks"]["Number"] += 1
            displayImage("rock.png", p=0)
            pygame_print("You got a rock!", 200)
        else:
            pygame_print("Nothing found.", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second


    elif setting.places[optionNumber] == "LANDSCAPE":
        Chances = randint(1, 100000)
        role.numInv["Sands"]["Number"] += 1
        displayImage("sand.png", p=0)
        pygame_print("You got SAND!", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second
        if Chances == 1:
            role.numInv["Sand Pails"]["Number"] += 1
            displayImage("sand pail.png", p=0)
            pygame_print("You found a sand pail!", 200)
        elif 2 <= Chances <= 11:
            role.numInv["Cactuses"]["Number"] += 1
            displayImage("cactus.png", p=0)
            pygame_print("You found a cactus!", 200, 0)
        else:
            pygame_print("Nothing else found.", 200)
        pygame.display.update()
        pygame.time.delay(1000)  # waiting one second

    role.searchTime = time()
    return setting.places[optionNumber]


def Stats(RoleHero):
    screen.fill(white)
    pygame_print(f"Attack Power = {RoleHero.attackpower:.0f}", 90)
    pygame_print(f"Health = {RoleHero.health:.0f} / {RoleHero.basehealth:.0f}", 130)
    pygame_print(f"Defense = {RoleHero.defense:.0f} / {RoleHero.baseDefense:.0f}", 170)
    pygame_print(f"Speed = {RoleHero.speed:.2f}", 210)
    pygame_print(f"Attack Stamina = {RoleHero.attackStamina}", 250)
    pygame_print(f"Defense Stamina = {RoleHero.defenseStamina}", 290)
    pygame_print(f"Money = {RoleHero.money}", 330)
    pygame_print(f"Quest Level = {RoleHero.questLevel}", 370)
    pygame_print(f"Stat Level = {RoleHero.currLevel:.0f}", 410)
    pygame_print(f"Exp = {RoleHero.currExp:.2f} / {RoleHero.LevelExp:.2f}", 450)
    pygame.display.update()
    while True:
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_RETURN:
                    print("exiting menu")
                    return


# prints a long pygame message
def long_pygame_print(message, count=0, line_break=24, color=black, background_color=white, offset=0, start_height=90):
    temp = ""
    # i is for indexing the string message
    message = message.split()
    for token in message:
        if len(temp + token) + 1 >= line_break:
            pygame_print(temp, loc=start_height + count, color=color, background_color=background_color, offset=offset)
            temp = token + " "
            count += 40
        else:
            temp += token + " "

    pygame_print(temp, loc=start_height + count, color=color, background_color=background_color, offset=offset)
    return count


def AddButton(text="STOP", offset=0, loc=36, background_color=red):
    global font
    font = pygame.font.Font('freesansbold.ttf', 26)
    stop_rect = pygame_print(text, loc=loc, background_color=background_color, offset=offset)
    font = pygame.font.Font('freesansbold.ttf', 32)

    return stop_rect


def Mine(role, setting):
    '''
    Objective: Click on the object before
    the NPC snatches the item (before npcTime elapses)
    '''
    # TODO: Make it so the rectangle is actually an item from the list of possible items that the user can mine

    screen.fill(white)
    global time, font
    TheSetting = setting.name.upper()
    message = "The objective of this game is to click on the item in time (To stop, type stop)!"
    Opponent = NeutralNPC()
    message += " Get ready, you are about to face"

    count = long_pygame_print(message)

    pygame_print(f"The {Opponent.role}", 90 + count)

    wins = 0
    losses = 0
    draws = 0
    totalplayerscore = 0
    playeravg = []
    botavg = []
    avgtime = []
    MinedItems = {}
    MinableItems = (
        "Sands", "Rocks", "Cactuses", "Sand Pails", "Logs", "Cookies", "Silvers", "Golds", "Diamonds", "Emeralds",
        "Golden Logs", "Golden Saplings")
    MineItemsProbs = (
        0.2657101102696958, 0.19928258270227184, 0.1328550551348479, 0.1328550551348479, 0.1328550551348479,
        0.1328550551348479, 0.001328550551348479, 0.0009299853859439353, 0.0006642752756742395, 0.00039856516540454366,
        0.0001328550551348479, 0.0001328550551348479)
    MineImagesDict = {'Sands': 'Assets/sand.png', 'Rocks': 'Assets/rock.png', 'Cactuses': 'Assets/cactus.png',
                      'Sand Pails': 'Assets/Sand Pail.png', 'Logs': 'Assets/log.png', 'Cookies': 'Assets/cookie.png',
                      'Silvers': 'Assets/silver.png', 'Golds': 'Assets/gold.png', 'Diamonds': 'Assets/diamond.png',
                      'Emeralds': 'Assets/emerald.png', 'Golden Logs': 'Assets/Golden Log.png',
                      'Golden Saplings': 'Assets/sapling.png'}
    pygame.display.update()

    # Each iteration corresponds to a respawn of an object
    # on the screen
    while True:
        screen.fill(white)

        font = pygame.font.Font('freesansbold.ttf', 20)
        pygame_print(f"Player Wins = {wins}", loc=100, offset=265)
        pygame_print(f"{Opponent.role} Wins = {losses}", loc=140, offset=265)
        pygame_print(f"Draws = {draws}", loc=180, offset=265)

        stop_rect = AddButton(offset=-100)

        pygame.draw.line(screen, black, (80, 75), (520, 75))  # top edge
        pygame.draw.line(screen, black, (80, 675), (520, 675))  # bottom edge
        pygame.draw.line(screen, black, (80, 75), (80, 675))  # left edge
        pygame.draw.line(screen, black, (520, 75), (520, 675))  # right edge

        pygame.display.update()
        # Determine coordinates where object will appear on the screen

        buffer_width = 40

        rand_X, rand_Y = randint(80 + buffer_width, 520 - buffer_width), randint(75 + buffer_width, 675 - buffer_width)

        square_rect = pygame.Rect(rand_X, rand_Y, buffer_width, buffer_width)

        item = np.random.choice(MinableItems, p=MineItemsProbs)
        image = pygame.image.load(MineImagesDict[item])
        image = pygame.transform.scale(image, (buffer_width, buffer_width))

        pygame.draw.rect(screen, white, square_rect)
        screen.blit(image, square_rect.topleft)

        pygame.display.update()
        #
        #        pygame.time.delay(1000)  # waiting one second

        start = time()
        npcTime = 1 + (1 * random())
        botavg.append(npcTime)
        breakFlag = False
        playerTime = None
        mouse_pos = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    playerTime = time() - start
                    breakFlag = True
                    break
            if breakFlag:
                break

        if stop_rect.collidepoint(mouse_pos):
            break

        # If the player clicked faster than the NPC and clicked correctly,
        # then the item is added to the inventory
        elif playerTime < npcTime and square_rect.collidepoint(mouse_pos):
            wins += 1
            totalplayerscore += 1
            botavg.append(npcTime)
            playeravg.append(playerTime)
            if item in MinedItems:
                MinedItems[item] += 1
            else:
                MinedItems[item] = 1
        elif playerTime > npcTime or not square_rect.collidepoint(mouse_pos):
            losses += 1
            totalplayerscore -= 1
            botavg.append(npcTime)
            playeravg.append(playerTime)
        elif playerTime == npcTime and square_rect.collidepoint(mouse_pos):  # Probably never happen
            draws += 1
            botavg.append(npcTime)
            playeravg.append(playerTime)

    #        pygame.time.delay(1000)  # waiting one second

    playeravglen = (len(playeravg)) if len(playeravg) != 0 else 1
    playeravg = sum(playeravg)
    botavglen = (len(botavg)) if len(botavg) != 0 else 1
    botavg = sum(botavg)
    points = wins - losses

    netExp = points * Opponent.expYield if points >= 0 else 0

    increaseExp(role, netExp)
    screen.fill(white)

    if playeravg / playeravglen < botavg / botavglen:
        pygame_print("You get 5 extra resources", 90)
        pygame_print("because your avg was better", 130)
        pygame_print(f"than the {Opponent.role}", 170)

        points += 5

    #        cookie              2-3     1-.1
    #        logs                3-4     .1-.01
    #        sands               0       100
    #        rocks               2       1
    #        silvers             4       .01
    #        golds               5       .001
    #        diamonds            7       .00001
    #        emeralds            7       .00001
    #        cactuses            3       .1
    #        golden saplings     8       .000001
    #        golden logs         8       .000001
    #        sand pails          5       .001

    for item in MinedItems:
        role.numInv[item]["Number"] += MinedItems[item]

    pygame_print("The player average is {:.2f} seconds".format(playeravg / playeravglen), loc=210)
    pygame_print("The {} average is {:.2f} seconds".format(Opponent.role, botavg / botavglen), loc=250)
    pygame_print("You got {} resources in total!".format(points), loc=290)
    pygame_print("You won {} games!".format(wins), loc=330)
    pygame_print("You lost {} games!".format(losses), loc=370)
    pygame_print("{} is the number of games that drawed!".format(draws), loc=410)

    pygame.display.update()
    while True:
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_RETURN:
                    return points


def printItem(role, item_name):
    global font, white, black, orange
    screen.fill(white)  # clear the screen

    #    pygame_print(f"{item}: {currentInventory[item]}", loc = line_count, color = orange if idx == optionNumber else black)
    #    print(role.useInv[item_name]["Use"]) #"Use" button
    #
    #    print(role.numInv[item_name]["Number"]) #The amount of the item
    #    print(role.numInv[item_name]["BuyValue"]) #The buy value of the item
    #    print(role.numInv[item_name]["SellValue"]) #The sell value of the item
    #    print(role.numInv[item_name]["QuestLevel"]) #The quest level at which this item is available
    #
    #    print(role.stringInv[item_name]["Name"]) #The name of the item
    #    print(role.stringInv[item_name]["Picture"]) #The picture of the item
    #    print(role.stringInv[item_name]["Description"]) #The description of the item
    #    print(role.stringInv[item_name]["Type"]) #The type of the item (e.g. healing, trading, etc.)

    square_rect = pygame.Rect(40, 100, 320, 235)  # left, top, width, height
    image = pygame.image.load(cppStringConvert(role.stringInv[item_name]["Picture"]))
    image = pygame.transform.scale(image, (320, 235))

    pygame.draw.rect(screen, white, square_rect)
    screen.blit(image, square_rect.topleft)

    pygame_print(f"Name: {item_name}", offset=-200, loc=380)
    pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset=-200, loc=440)
    long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset=-200,
                      line_break=23, start_height=550)

    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset=200, loc=200)
    pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset=200, loc=260)
    pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset=200, loc=320)
    pygame_print(f"Quest Level: {role.numInv[item_name]['QuestLevel']}", offset=200, loc=380)

    rect = AddButton(text="Use", offset=200, loc=550, background_color=orange)

    pygame.display.update()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:  # checking if the mouse was clicked on the window
                mouse_pos = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_pos):
                    print("Using the item.")
                    role.useInv[item_name]["Use"]()
                    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset=200, loc=200)
                    pygame.display.update()


def getItemCounts(role):
    line_count = 80
    currentInventory = {}
    for item in role.numInv:
        for attr in item.second:
            if cppStringConvert(attr.first) == "Number" and attr.second > 0:
                item_name = cppStringConvert(item.first)
                pygame_print(f"{item_name}: {attr.second}", loc=line_count, color=orange if line_count == 80 else black)
                currentInventory[item_name] = attr.second
                line_count += 40

    return currentInventory, (line_count - 80) // 40


def printInventory(role):
    global font, white, black, orange
    screen.fill(white)

    currentInventory, num_items = getItemCounts(role)

    # If the user doesn't have any items, then we need to handle this differently.
    if num_items == 0:
        pygame_print("You don't have any items.", )
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

    currentInventoryList = list(currentInventory.keys())
    line_count = 80
    stop_rect = AddButton(text="EXIT", offset=0)
    optionNumber = 0
    pygame.display.update()

    while True:
        screen.fill(white)
        line_count = 80
        currentInventory, num_items = getItemCounts(role)
        currentInventoryList = list(currentInventory.keys())
        for idx, item in enumerate(currentInventory):
            pygame_print(f"{item}: {currentInventory[item]}", loc=line_count,
                         color=orange if idx == optionNumber else black)
            line_count += 40

        stop_rect = AddButton(text="EXIT", offset=0)
        pygame.display.update()

        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != num_items - 1 else 0
                elif event.key == pygame.K_UP:
                    optionNumber = optionNumber - 1 if optionNumber != 0 else num_items - 1
                elif event.key == pygame.K_RETURN:
                    print(currentInventoryList[optionNumber])  # item that the user is hovering on
                    printItem(role, currentInventoryList[optionNumber])
            elif event.type == pygame.MOUSEBUTTONDOWN:  # checking if the mouse was clicked on the window
                mouse_pos = pygame.mouse.get_pos()
                if stop_rect.collidepoint(mouse_pos):
                    return


class Shot:
    def __init__(self, beam_x, beam_y, hit_target, is_flipped):
        self.beam_x = beam_x
        self.beam_y = beam_y
        self.hit_target = hit_target
        self.is_flipped = is_flipped


def QuestGames(Setting, role):
    global font, white, black, orange, X, Y, red

    role_image_name = role.name.lower().replace(" jackson", "") + "-start.png"
    role_image_name_flipped = role_image_name.replace(".png", "flip.png")
    enemy_image_names = {"NINJA": "ninja.png", "OGRE": "ogre.png", "DEMON": "demon.png"}
    enemy_image_names_flipped = {"NINJA": "ninjaflip.png", "OGRE": "ogreflip.png", "DEMON": "demonflip.png"}

    buffer_width = 40

    start_x, start_y, curr_y, enemy_x, enemy_y, curr_enemy_y = 100, 600, 600, 650, 600, 600
    ground_y = 600

    role_jump_t, enemy_jump_t = -1, -1

    role_rect, enemy_rect = None, None
    print(Setting := Setting.name.upper())

    def spawnBadNPC():
        randnum = randint(1, 100)
        print(randnum)
        start = 1
        end = 0
        for b in badNPCs:
            end += int(b.second * 100)  # probability of spawning
            if start <= randnum <= end:
                a = BadNPC(cppStringConvert(b.first))  # we are spawning an enemy here
                a.statboost(role)
                return a

    a = spawnBadNPC()
    print(f"Enemy name = {a.name}, enemy_image_names.get(a.name) = {enemy_image_names.get(a.name)}")

    def renderRole(start_x, start_y):
        # TODO: Fix the backdrop so it doesn't slow down the quest
        if Setting == "DESERT":
            displayImage("StartDesert.png", p=1, update=False)
        elif Setting == "FOREST":
            displayImage("StartForest.png", p=1, update=False)
        elif Setting == "MOUNTAIN":
            displayImage("StartMountain.png", p=1, update=False)
        elif Setting == "BEACH":
            displayImage("StartBeach.png", p=1, update=False)
        elif Setting == "HOUSE":
            displayImage("StartHouse.png", p=1, update=False)
        #        screen.fill(white)
        pygame_print(f"Quest #{role.questLevel + 1}", loc=60)
        # Role
        role_image = pygame.image.load(
            f"Assets/{role_image_name}" if not role.flipped else f"Assets/{role_image_name_flipped}")
        role_image = pygame.transform.scale(role_image, (buffer_width, buffer_width))
        screen.blit(role_image, role_rect.topleft)
        # Enemy
        enemy_image = pygame.image.load(
            f"Assets/{enemy_image_names[a.name]}" if not a.flipped else f"Assets/{enemy_image_names_flipped[a.name]}")
        enemy_image = pygame.transform.scale(enemy_image, (buffer_width, buffer_width))
        screen.blit(enemy_image, enemy_rect.topleft)

    role_rect = pygame.Rect(start_x, start_y, buffer_width, buffer_width)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, buffer_width, buffer_width)
    renderRole(start_x, start_y)

    shotsFired = deque([], maxlen=10)
    shotsEnemyFired = deque([], maxlen=10)
    beam_y_offset = -5  # TODO: Maybe adjust this to see if there's a better value
    # TODO: Add beam_x_offset to make it emanate closer to shooter
    beam_x_offset = -12.5
    K = 10  # Constant factor

    global badNPCs  # we're saying that we will be using the global variable badNPCs
    NumberDefeated = 0
    expEarned = 0  # TODO: Update XP

    enemy_options = ("attack", "left", "right", "jump")

    while True:  # pygame loop
        enemyMove = randint(0, 3)
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_SPACE:  # Checking if the role hero fired a shot
                    # Put beam on the screen if role has the stamina for it
                    if role.can_attack():
                        # 100 - (27.5) = 72.5 or 100 + (40-12.5) = 127.5
                        beam_x = start_x - ((buffer_width + beam_x_offset) if not role.flipped else (-buffer_width))
                        beam_y = curr_y + buffer_width + beam_y_offset
                        # Puts the coordinate of the shots fired on the screen
                        shotsFired.append(Shot(beam_x, beam_y, False,
                                               role.flipped))  # x-position of beam, y-position of beam, has it hit the target?, flipped?
                        # Update the wait-time here.
                        role.update_wait_time()

        if enemy_options[enemyMove] == "jump" and enemy_y + 200 >= ground_y:  # Holding down jump makes it bigger
            curr_enemy_y -= 5
            enemy_y = curr_enemy_y
            enemy_jump_t = time()
        if enemy_options[enemyMove] == "attack" and a.can_attack():
            # If the offset problem is the direction their shooting, get rid of 1st beam_x_offset, else if it's the flipped image, get rid of 2nd beam_x_offset
            beam_x = enemy_x + ((buffer_width + beam_x_offset) if not a.flipped else (-buffer_width - beam_x_offset))
            beam_y = curr_enemy_y + buffer_width + beam_y_offset
            # Puts the coordinate of the shots fired on the screen
            shotsEnemyFired.append(Shot(beam_x, beam_y, False,
                                        a.flipped))  # x-position of beam, y-position of beam, has it hit the target?, flipped?
            a.update_wait_time()

        keys = pygame.key.get_pressed()
        # -> means 0.01 s, the below example shows how our position changes ever 0.01 seconds when falling
        '''
        95 -> 95.004905 -> 95.01962 -> 95.044145 -> 95.07848 -> 95.122625 -> 95.17658 -> 95.240345 -> 95.31392 -> 95.397305 -> 95.4905 -> 95.593505 -> 95.70632 -> 95.828945 -> 95.96138 -> 96.103625 -> 96.25568 -> 96.417545 -> 96.58922 -> 96.770705 -> 96.962 -> 97.163105 -> 97.37402 -> 97.594745 -> 97.82528 -> 98.065625 -> 98.31578 -> 98.575745 -> 98.84552000000001 -> 99.125105 -> 99.4145 -> 99.713705 -> 100.02272 -> 100.34154500000001 -> 100.67018 -> 101.00862500000001 -> 101.35688 -> 101.714945 -> 102.08282000000001 -> 102.46050500000001 -> 102.84800000000001 -> 103.245305 -> 103.65242 -> 104.06934500000001 -> 104.49608 -> 104.93262500000002 -> 105.37898000000001 -> 105.83514500000001 -> 106.30112000000001 -> 106.77690500000001 -> 107.26250000000002 -> 107.75790500000001 -> 108.26312000000001 -> 108.77814500000001 -> 109.30298000000002 -> 109.83762500000002 -> 110.38208000000002 -> 110.93634500000002 -> 111.50042000000002 -> 112.07430500000002 -> 112.65800000000002 -> 113.25150500000002 -> 113.85482000000002 -> 114.46794500000001 -> 115.09088000000003 -> 115.72362500000003 -> 116.36618000000003 -> 117.01854500000003 -> 117.68072000000004 -> 118.35270500000003 -> 119.03450000000004 -> 119.72610500000003 -> 120.42752000000003 -> 121.13874500000003 -> 121.85978000000003 -> 122.59062500000003 -> 123.33128000000004 -> 124.08174500000004 -> 124.84202000000003 -> 125.61210500000004 -> 126.39200000000004 -> 127.18170500000005 -> 127.98122000000004 -> 128.79054500000004 -> 129.60968000000005 -> 130.43862500000006 -> 131.27738000000005 -> 132.12594500000006 -> 132.98432000000005 -> 133.85250500000006 -> 134.73050000000006 -> 135.61830500000005 -> 136.51592000000005 -> 137.42334500000007 -> 138.34058000000005 -> 139.26762500000007 -> 140.20448000000005 -> 141.15114500000007 -> 142.10762000000005 -> 143.07390500000008

        orig_height = height = 95
        s=lambda x: 5*9.81*x**2
        count = 0
        for i in range(1,101):
            print(f"{height}", end = " -> ")
            count += 0.01
            height = s(count)+orig_height
        '''

        if curr_y != ground_y:  # if the hero is in free-fall
            fall_time = time() - role_jump_t
            s = K * 0.5 * 9.81 * fall_time ** 2  # The absolute value the hero has fallen since role_jump_t

            '''
            Example: You fell from a cliff 2 km above sea-level at 10:00:00.
            Question: How far have you fallen at 10:00:10?
            Answer:
                s = 0.5*9.81*(10:00:10 - 10:00:00)**2 = 0.5*9.81*10**2 = 0.5*9.81*100 = 490.5 meters ~ 1/2 of a km
            '''
            position = start_y + s
            if position <= ground_y:  # If they are still falling
                curr_y = position
            else:  # Here, they have landed
                curr_y = ground_y
                start_y = ground_y
        if curr_enemy_y != ground_y:
            fall_time = time() - enemy_jump_t
            s = K * 0.5 * 9.81 * fall_time ** 2
            position = enemy_y + s
            if position <= ground_y:
                curr_enemy_y = position
            else:
                curr_enemy_y = ground_y
                enemy_y = ground_y

        # If the role moves across the screen (left or right)
        # ===================================================
        if keys[pygame.K_RIGHT]:  # if right arrow was pressed, move right
            if start_x < X - 40:
                start_x += role.speed * 20
            role.flipped = False
        if keys[pygame.K_LEFT]:  # if left arrow was pressed, move left
            if start_x > 0:
                start_x -= role.speed * 20
            role.flipped = True
        if keys[pygame.K_UP]:
            if curr_y + 200 >= ground_y:  # Check if they can keep going higher, curr_y must >= 400 atm (less than 200 elevation)
                curr_y -= 5
                start_y = curr_y  # Set the start jumping position to the current position
                role_jump_t = time()

        if enemy_options[enemyMove] == "right":
            if enemy_x < X - 40:
                enemy_x += a.speed * 10
            a.flipped = True
        if enemy_options[enemyMove] == "left":
            if enemy_x > 0:
                enemy_x -= a.speed * 10
            a.flipped = False

        role_rect = pygame.Rect(start_x, curr_y, buffer_width, buffer_width)
        enemy_rect = pygame.Rect(enemy_x, curr_enemy_y, buffer_width, buffer_width)
        renderRole(start_x, curr_y)

        for shot in shotsFired:
            shot.beam_x = shot.beam_x + 50 if not shot.is_flipped else shot.beam_x - 50  # TODO: make the shot speed depend on the role's stats?
            beam_rect = pygame.Rect(shot.beam_x, shot.beam_y, buffer_width / 2,
                                    buffer_width / 4)  # beam object
            if beam_rect.colliderect(
                    enemy_rect) and not shot.hit_target:  # Enemy was hit and this is not a repeat of the same shot
                role.attack(a)
                print(f"Enemy health = {a.health:.2f}")
                if a.health <= 0:
                    print("Spawning new enemy")
                    a = spawnBadNPC()
                    NumberDefeated += 1
                shot.hit_target = True
            pygame.draw.ellipse(screen, orange, beam_rect)  # Drawing the beam

        for shot in shotsEnemyFired:
            shot.beam_x = shot.beam_x - 41 if not shot.is_flipped else shot.beam_x + 63  # TODO: make the shot speed depend on the role's stats? HW: Change 50 to something smaller to debug
            beam_rect = pygame.Rect(shot.beam_x, shot.beam_y, buffer_width / 2,
                                    buffer_width / 4)  # beam object
            if beam_rect.colliderect(
                    role_rect) and not shot.hit_target:  # Role was hit and this is not a repeat of the same shot
                a.attack(role)
                print(f"Role health = {role.health:.2f}")
                if role.health <= 0:
                    print("You died!")
                    return
                shot.hit_target = True
            pygame.draw.ellipse(screen, red, beam_rect)  # Drawing the beam

        pygame.display.update()

        if NumberDefeated == 10 or role.health <= 0:
            # Do stuff
            return


def Menu(role, setting):
    # Only going to execute once
    global Quests, orange, black, white, X
    if Quests == False:
        optionNumber = 0
        pygame.display.update()

        while True:
            #            screen.fill(white)
            pygame_print("Choose an option", 90, color=black, background_color=white)
            pygame_print("================", 130, color=black, background_color=white)
            pygame_print("Map", 170, color=(orange if optionNumber == 0 else black), background_color=white)
            pygame_print("Search", 210, color=(orange if optionNumber == 1 else black), background_color=white)
            pygame_print("Stats", 250, color=(orange if optionNumber == 2 else black), background_color=white)
            pygame.display.update()
            for event in pygame.event.get():  # update the option number if necessary
                if event.type == pygame.KEYDOWN:  # checking if any key was selected
                    if event.key == pygame.K_DOWN:
                        optionNumber = optionNumber + 1 if optionNumber != 2 else 0
                    elif event.key == pygame.K_UP:
                        optionNumber = optionNumber - 1 if optionNumber != 0 else 2
                    elif event.key == pygame.K_RETURN:
                        if optionNumber == 0:  # Map
                            setting.map()
                        elif optionNumber == 1:  # Search
                            search(setting, role)
                        elif optionNumber == 2:  # Stats
                            Stats(role)
                        return

    # Will go on until user enters "Quests"
    elif Quests == True or Shop == True:
        '''
        Enter one of the following options
        ==================================

        '''
        optionNumber = 0
        pygame.display.update()
        while True:
            screen.fill(white)
            pygame_print("Choose an option", 90, color=black, background_color=white)
            pygame_print("================", 130, color=black, background_color=white)
            pygame_print("Map", 170, color=(orange if optionNumber == 0 else black), background_color=white)
            pygame_print("Search", 210, color=(orange if optionNumber == 1 else black), background_color=white)
            pygame_print("Mine", 250, color=(orange if optionNumber == 2 else black), background_color=white)
            pygame_print("Inv", 290, color=(orange if optionNumber == 3 else black), background_color=white)
            pygame_print("Shop", 330, color=(orange if optionNumber == 4 else black), background_color=white)
            pygame_print("Quests", 370, color=(orange if optionNumber == 5 else black), background_color=white)
            pygame_print("Stats", 410, color=(orange if optionNumber == 6 else black), background_color=white)
            pygame.display.update()
            for event in pygame.event.get():  # update the option number if necessary
                if event.type == pygame.KEYDOWN:  # checking if any key was selected
                    if event.key == pygame.K_DOWN:
                        optionNumber = optionNumber + 1 if optionNumber != 6 else 0
                    elif event.key == pygame.K_UP:
                        optionNumber = optionNumber - 1 if optionNumber != 0 else 6
                    elif event.key == pygame.K_RETURN:
                        if optionNumber == 0:  # Map
                            setting.map()
                        elif optionNumber == 1:  # Search
                            search(setting, role)
                        elif optionNumber == 2:  # Mine
                            Mine(role, setting)
                        elif optionNumber == 3:  # Inventory
                            printInventory(role)
                        elif optionNumber == 4:  # Shop
                            pass
                        elif optionNumber == 5:  # Quests
                            QuestGames(setting, role)
                        elif optionNumber == 6:  # Stats
                            Stats(role)
                        return

        option = cS(input(
            "Enter one of the following options\n==================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))

        # Input validation
        while option not in ("MAP", "SEARCH", "QUESTS", "MINE", "INV", "SHOP", "STATS"):
            print("Try again!")
            option = cS(input(
                "Enter one of the following options\n==================================\n'Map'\n'Search'\n'Mine'\n'Inv'\n'Shop'\n'Quests'\n'Stats'\n\n"))

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
                ProcessInvRequest(role)
                option = GetMenuOption()
            elif option == "SHOP":
                if Shop == True:
                    shop(role)
                    option = GetMenuOption()
                else:
                    print("You do not have access to the shop yet!")
                    option = GetMenuOption()


def game():
    # TODO: uncomment next line in actual game
    # slowPrint("Welcome to the Game!")
    global font, Quests
    try:
        pygame.display.set_caption('Game Window')
        text = font.render('Welcome to the Game!', True, black, light_pink)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)
        start = time()
        started = False
        displayedHeroes = False
        dispayedChest = False
        displayedPlaces = False
        optionNumber = 3  # (3, 4, or 5)
        updated = False
        playerhero = ""  # declare the hero that the user wants to be
        heroes = displayHeroes()
        YesNo = ("Yes", "No")
        RoleHero = None
        Place = None

        while True:
            pygame.display.update()
            for event in pygame.event.get():  # Can only call pygame.event.get() once per iteration
                if not started:
                    screen.fill(light_pink)
                    screen.blit(text, textRect)
                    pygame.display.update()
                    started = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif not displayedHeroes:
                    pygame.time.delay(1000)
                    updateList(heroes, optionNumber)
                    displayedHeroes = True
                elif displayedHeroes and not dispayedChest:
                    if event.type == pygame.KEYDOWN:  # checking if any key was selected
                        if event.key == pygame.K_DOWN:
                            optionNumber = optionNumber + 1 if optionNumber != 5 else 3
                            updateList(heroes, optionNumber)  # update screen
                        elif event.key == pygame.K_UP:
                            optionNumber = optionNumber - 1 if optionNumber != 3 else 5
                            updateList(heroes, optionNumber)  # update screen
                        elif event.key == pygame.K_RETURN:
                            playerhero = heroes[optionNumber]
                            pygame.event.clear(
                                eventtype=pygame.KEYDOWN)  # https://www.pygame.org/docs/ref/event.html#pygame.event.get
                            if playerhero == "PERCY JACKSON":
                                displayImage("percy-start.png", p=1)
                                pygame.time.delay(2000)
                                RoleHero = PercyJackson(playerhero)
                            elif playerhero == "ELF":
                                displayImage("elf-start.png", p=1)
                                pygame.time.delay(2000)
                                RoleHero = Elf(playerhero)
                            elif playerhero == "ZELDA":
                                displayImage("zelda-start.png", p=1)
                                pygame.time.delay(2000)
                                RoleHero = Zelda(playerhero)

                            optionNumber = 0  # set the variable for the next option menu

                            screen.fill(white)
                            text = font.render("Where am I?", True, black, white)
                            textRect = text.get_rect()
                            textRect.center = (X // 2, Y // 1.5)
                            screen.blit(text, textRect)
                            pygame.display.update()
                            pygame.time.delay(1000)
                            displayImage("treasure_chest.png", p=1)
                            pygame.time.delay(2000)

                            text = font.render("You see a chest", True, black, white)
                            textRect = text.get_rect()
                            textRect.center = (X // 2, Y // 1.5)
                            screen.blit(text, textRect)
                            pygame.display.update()

                            pygame.time.delay(1000)  # Can change later

                            text = font.render("Do you open the chest?", True, black, white)
                            textRect = text.get_rect()
                            textRect.center = (X // 2, Y // 1.5)
                            screen.blit(text, textRect)
                            pygame.display.update()

                            pygame.time.delay(250)
                            openChestOption(optionNumber)  # Displaying 'Yes' and 'No'
                            dispayedChest = True
                            pygame.event.clear(
                                eventtype=pygame.KEYDOWN)  # We don't want the enter that they press to do anything until 'Yes' and 'No' are displayed

                elif dispayedChest and not displayedPlaces:

                    if event.type == pygame.KEYDOWN:  # checking if any key was selected
                        # optionNumber: Yes = 0, No = 1
                        if event.key == pygame.K_DOWN:
                            optionNumber = optionNumber + 1 if optionNumber != 1 else 0
                            openChestOption(optionNumber)

                        elif event.key == pygame.K_UP:
                            optionNumber = optionNumber - 1 if optionNumber != 0 else 1
                            openChestOption(optionNumber)

                        elif event.key == pygame.K_RETURN:
                            if optionNumber == 0:  # Yes
                                displayImage("treasure_chest.png", p=1)

                                text = font.render("You do not have the key!", True, black, white)
                                textRect = text.get_rect()
                                textRect.center = (X // 2, Y // 1.5)
                                screen.blit(text, textRect)
                                pygame.display.update()

                                pygame.time.delay(1000)  # Can change later

                            screen.fill(white)
                            pygame.display.update()
                            displayedPlaces = True
                            optionNumber = 0

                        pygame.event.clear(
                            eventtype=pygame.KEYDOWN)  # Clear any keys that were pressed in this if-block

                elif displayedPlaces and not Quests:
                    font = pygame.font.Font('freesansbold.ttf', 28)
                    text = font.render("Where do you want to go?", True, black, white)
                    textRect = text.get_rect()
                    textRect.center = (X // 2, 50)
                    screen.blit(text, textRect)
                    text = font.render("========================", True, black, white)
                    textRect = text.get_rect()
                    textRect.center = (X // 2, 90)
                    screen.blit(text, textRect)
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    PlaceOption(optionNumber)
                    pygame.display.update()
                    if event.type == pygame.KEYDOWN:  # checking if any key was selected
                        if event.key == pygame.K_DOWN:
                            optionNumber = optionNumber + 1 if optionNumber != 4 else 0
                            PlaceOption(optionNumber)  # update screen
                        elif event.key == pygame.K_UP:
                            optionNumber = optionNumber - 1 if optionNumber != 0 else 4
                            PlaceOption(optionNumber)  # update screen
                        elif event.key == pygame.K_RETURN:
                            if optionNumber == 0:
                                print("House")
                                displayImage("StartHouse.png", p=1)
                                pygame.time.delay(2000)
                                Place = House()
                            elif optionNumber == 1:
                                print("Beach")
                                displayImage("StartBeach.png", p=1)
                                pygame.time.delay(2000)
                                Place = Beach()
                            elif optionNumber == 2:
                                print("Forest")
                                displayImage("StartForest.png", p=1)
                                pygame.time.delay(2000)
                                Place = Forest()
                            elif optionNumber == 3:
                                print("Mountain")
                                displayImage("StartMountain.png", p=1)
                                pygame.time.delay(2000)
                                Place = Mountain()
                            elif optionNumber == 4:
                                print("Desert")
                                displayImage("StartDesert.png", p=1)
                                pygame.time.delay(2000)
                                Place = Desert()
                            pygame.event.clear(
                                eventtype=pygame.KEYDOWN)  # Clear any keys that were pressed in this if-block before displaying the menu
                            Menu(RoleHero, Place)
                            Quests = True
                            pygame.display.update()

                            screen.fill(white)
                            font = pygame.font.Font('freesansbold.ttf', 32)
                            text = font.render("New things unlocked!", True, black, white)
                            textRect = text.get_rect()
                            textRect.center = (X // 2, 90)
                            screen.blit(text, textRect)
                            pygame.display.update()
                            pygame.time.delay(500)

                            screen.fill(white)
                            font = pygame.font.Font('freesansbold.ttf', 26)
                            text = font.render("Quests have been unlocked.", True, black, white)
                            textRect = text.get_rect()
                            textRect.center = (X // 2, 90)
                            screen.blit(text, textRect)
                            pygame.display.update()
                            pygame.time.delay(500)

                            screen.fill(white)
                            text = font.render("To open quests", True, black, white)
                            textRect = text.get_rect()
                            textRect.center = (X // 2, 70)
                            screen.blit(text, textRect)
                            pygame.display.update()
                            pygame.time.delay(500)
                            font = pygame.font.Font('freesansbold.ttf', 28)
                            text = font.render("Select 'Quests' in the menu", True, black, white)
                            textRect = text.get_rect()
                            textRect.center = (X // 2, 120)
                            font = pygame.font.Font('freesansbold.ttf', 32)
                            screen.blit(text, textRect)
                            pygame.display.update()
                            pygame.time.delay(1000)

                            pygame.event.clear(
                                eventtype=pygame.KEYDOWN)  # Clear any keys that were pressed in this if-block
                elif Quests:
                    while True:
                        Menu(RoleHero, Place)

        # Animation

        HeroGame(playerhero)

    except KeyboardInterrupt:
        print("\nBye")
        # TODO: Save Here


game()