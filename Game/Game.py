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
from collections import deque, namedtuple
from math import sqrt, log as ln
import json

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
# Find out where we can increase money besides selling ✅


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
        double base_health;
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
            this->base_health = 100.0;
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
            this->base_health = 500.0;
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
            this->base_health = 100.0;
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
        double base_health;
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
        std::unordered_map<std::string, double> printBuyItems(bool print = true);
        std::vector<std::string> printBuyItemsVec(bool print = true);
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

        Role(std::string name);
        virtual ~Role();
    };

    void BadNPC::attack(Role& RoleHero)
    {
        RoleHero.health -= (Defense(RoleHero.defense) * attackpower);
        if (RoleHero.health < 0)
        {
            RoleHero.health = 0;
        }
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
        enemy.health -= (Defense(enemy.defense) * attackpower); //the enemy's health can go below 0, so see below :)
        if (enemy.health < 0)
        {
            enemy.health = 0;
        }
    }

    void Role::baseLineStats()
    {
        std::cout << "\nAttack Power = " << std::setprecision(0)
        << std::fixed << attackpower << '\n'
        << "Health = " << std::setprecision(0)
        << std::fixed << health << " / " << std::setprecision(0)
        << std::fixed << base_health << '\n'
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
        base_health = multiplier * base_health;
        defense = multiplier * defense;
        expYield = multiplier * expYield;
        speed = multiplier * speed;
        attackStamina = attackStamina / multiplier;
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

    //print = true, prints out AND returns vecotr
    //print = false, ONLY returns vector, doesn't print anything
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

    std::unordered_map<std::string, double> Role::printBuyItems(bool print)
    {
        std::unordered_map<std::string, double> buyableItems;
        if (print)
        {
            std::cout << std::setw(20) << "Item" << std::setw(20) << "Picture" <<
                    std::setw(20) << "Buy Value" << '\n' << std::setw(20) << "----" << std::setw(20) << "-------" << std::setw(20) << "---------" << '\n';
        }

        for (auto& i: stringInv)
        {
        //            "Item", "Picture", "Buy Value"
            if ((numInv[i.first].find("BuyValue") != numInv[i.first].end()) && (numInv[i.first]["Questlevel"] <= this->questLevel) &&
                (this->money >= numInv[i.first]["BuyValue"]))
            {
                if (print)
                {
                    std::cout << std::setw(20) << stringInv[i.first]["Name"] << std::setw(20) << stringInv[i.first]["Picture"] << std::setw(20) << numInv[i.first]["BuyValue"] << std::setw(20) << '\n';
                }
                std::string temp = i.first;
                std::transform(temp.begin(), temp.end(),temp.begin(), ::toupper);
                buyableItems[temp] = numInv[i.first]["BuyValue"];
            }
        }
        if (print)
        {
            std::cout << '\n';
        }
        return buyableItems;
    }
    
    std::vector<std::string> Role::printBuyItemsVec(bool print)
    {
        std::vector<std::string> buyableItems;
        if (print)
        {
            std::cout << std::setw(20) << "Item" << std::setw(20) << "Picture" <<
                    std::setw(20) << "Buy Value" << '\n' << std::setw(20) << "----" << std::setw(20) << "-------" << std::setw(20) << "---------" << '\n';
        }

        for (auto& i: stringInv)
        {
        //            "Item", "Picture", "Buy Value"
            if ((numInv[i.first].find("BuyValue") != numInv[i.first].end()) && (numInv[i.first]["Questlevel"] <= this->questLevel) &&
                (this->money >= numInv[i.first]["BuyValue"]))
            {
                if (print)
                {
                    std::cout << std::setw(20) << stringInv[i.first]["Name"] << std::setw(20) << stringInv[i.first]["Picture"] << std::setw(20) << numInv[i.first]["BuyValue"] << std::setw(20) << '\n';
                }
                buyableItems.push_back(i.first);
            }
        }
        if (print)
        {
            std::cout << '\n';
        }
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
        base_health = 0;
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
                        "Potion",{{"Name", "Potion"}, {"Picture", "Assets/potion.png"}, {"Description", "A potion, maybe you can drink it (Increases health by 20)"}, {"Type", "Healing"}}
                },

                {
                        "Apple",{{"Name", "Apple"}, {"Picture", "Assets/apple.png"}, {"Description", "An apple, maybe you can eat it (Increases health by 10)! "}, {"Type", "Healing"}}
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
                                       if (health > base_health)
                                       {
                                           health = base_health;
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
                                       if (this->health > base_health)
                                       {
                                           health = base_health;
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
                                       if (this->health > base_health)
                                       {
                                           health = base_health;
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
        self.base_health = 200
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
        self.base_health = 50
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
        self.base_health = 100
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
    role.base_health += role.HealthLevelFunc(role.currLevel)
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


def displayHeroes(printing=False):
    lines = ["------", "Heroes", "------"]
    for hero in heroes:
        lines.append(hero)
    lines.append("")
    print("\n".join(lines)) if not printing else print()
    return lines

#################################################################################################

pygame.init()
white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (0, 128, 0)
blue = (0, 0, 128)
cyan = (0, 255, 255)
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
    pygame_print(f"Health = {RoleHero.health:.0f} / {RoleHero.base_health:.0f}", 130)
    pygame_print(f"Defense = {RoleHero.defense:.0f} / {RoleHero.baseDefense:.0f}", 170)
    pygame_print(f"Speed = {RoleHero.speed:.2f}", 210)
    pygame_print(f"Attack Stamina = {RoleHero.attackStamina:.2f}", 250)
    pygame_print(f"Defense Stamina = {RoleHero.defenseStamina:.2f}", 290)
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
                    return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:  # checking if the mouse was clicked on the window
                mouse_pos = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_pos):
                    print("Using the item.")
                    role.useInv[item_name]["Use"]()
                    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset=200, loc=200)
                    pygame.display.update()

def sellItem(role, item_name):
    global font, white, black, orange
    screen.fill(white)  # clear the screen

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
    pygame_print(f"Your Money:", offset=200, loc=380)
    font = pygame.font.Font('freesansbold.ttf', 25)
    pygame_print(f"{role.money:.2f}", offset=200, loc=440)
    font = pygame.font.Font('freesansbold.ttf', 32)

    num_item = 0 #Count the amount of item_name that the user wants to buy
    max_amount = int(role.numInv[item_name]['Number'])
    pygame_print(f"How many?: {num_item}", offset=200, loc=550)

    rect = AddButton(text="Sell", offset=200, loc=630, background_color=green)

    pygame.display.update()

    while True:
        
        screen.fill(white)  # clear the screen
        pygame.draw.rect(screen, white, square_rect)
        screen.blit(image, square_rect.topleft)

        pygame_print(f"Name: {item_name}", offset=-200, loc=380)
        pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset=-200, loc=440)
        long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset=-200,
                  line_break=23, start_height=550)

        pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset=200, loc=200)
        pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset=200, loc=260)
        pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset=200, loc=320)
        pygame_print(f"Your Money:", offset=200, loc=380)
        font = pygame.font.Font('freesansbold.ttf', 25)
        pygame_print(f"{role.money:.2f}", offset=200, loc=440)
        font = pygame.font.Font('freesansbold.ttf', 32)
        pygame_print(f"How many?: {num_item}", offset=200, loc=550)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 0
                elif event.key == pygame.K_DOWN:
                    num_item = num_item - 1 if num_item != 0 else max_amount
                elif event.key == pygame.K_UP:
                    num_item = num_item + 1 if num_item != max_amount else 0
            elif event.type == pygame.MOUSEBUTTONDOWN:  # checking if the mouse was clicked on the window
                mouse_pos = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_pos):
                    print("Selling the item.")
                    role.numInv[item_name]['Number'] -= num_item
                    role.money += num_item * role.numInv[item_name]['SellValue']
                    max_amount = int(role.numInv[item_name]['Number'])
                    num_item = 0
            elif rect.collidepoint(pygame.mouse.get_pos()):
                rect = AddButton(text="Sell", offset=200, loc=630, background_color=orange)
                pygame.display.update()
            elif not rect.collidepoint(pygame.mouse.get_pos()):
                rect = AddButton(text="Sell", offset=200, loc=630, background_color=green)
                pygame.display.update()

def buyItem(role, item_name):
    global font, white, black, orange
    screen.fill(white)  # clear the screen

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
    pygame_print(f"Your Money:", offset=200, loc=380)
    font = pygame.font.Font('freesansbold.ttf', 25)
    pygame_print(f"{role.money:.2f}", offset=200, loc=440)
    font = pygame.font.Font('freesansbold.ttf', 32)

    num_item = 0 #Count the amount of item_name that the user wants to buy
    max_amount = int(role.money // role.numInv[item_name]['BuyValue'])
    pygame_print(f"How many?: {num_item}", offset=200, loc=550)

    pygame.display.update()
    rect = AddButton(text="Buy", offset=200, loc=630, background_color=green)
    
    while True:
        
        screen.fill(white)  # clear the screen
        pygame.draw.rect(screen, white, square_rect)
        screen.blit(image, square_rect.topleft)

        pygame_print(f"Name: {item_name}", offset=-200, loc=380)
        pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset=-200, loc=440)
        long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset=-200,
                  line_break=23, start_height=550)

        pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset=200, loc=200)
        pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset=200, loc=260)
        pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset=200, loc=320)
        pygame_print(f"Your Money:", offset=200, loc=380)
        font = pygame.font.Font('freesansbold.ttf', 25)
        pygame_print(f"{role.money:.2f}", offset=200, loc=440)
        font = pygame.font.Font('freesansbold.ttf', 32)
        pygame_print(f"How many?: {num_item}", offset=200, loc=550)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 0
                elif event.key == pygame.K_DOWN:
                    num_item = num_item - 1 if num_item != 0 else max_amount
                elif event.key == pygame.K_UP:
                    num_item = num_item + 1 if num_item != max_amount else 0
            elif event.type == pygame.MOUSEBUTTONDOWN:  # checking if the mouse was clicked on the window
                mouse_pos = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_pos):
                    print("Buying the item.")
                    role.numInv[item_name]['Number'] += num_item
                    role.money -= num_item * role.numInv[item_name]['BuyValue']
                    max_amount = int(role.money // role.numInv[item_name]['BuyValue'])
                    num_item = 0
            elif rect.collidepoint(pygame.mouse.get_pos()):
                rect = AddButton(text="Buy", offset=200, loc=630, background_color=orange)
                pygame.display.update()
            elif not rect.collidepoint(pygame.mouse.get_pos()):
                rect = AddButton(text="Buy", offset=200, loc=630, background_color=green)
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

    def print_no_items():
        pygame_print("You don't have any items.", )
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

    screen.fill(white)

    currentInventory, num_items = getItemCounts(role)

    # If the user doesn't have any items, then we need to handle this differently.
    if num_items == 0:
        print_no_items()
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
        if num_items == 0:
            print_no_items()
            return
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
                    print(f"optionNumber = {optionNumber}")
                    print(currentInventoryList[optionNumber])  # item that the user is hovering on
                    optionNumber = printItem(role, currentInventoryList[optionNumber])
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
    role.health = role.base_health  # TODO: delete!
    role.attackpower = 1000  # TODO: delete!
    money = 0

    role_image_name = role.name.lower().replace(" jackson", "") + "-start.png"
    role_image_name_flipped = role_image_name.replace(".png", "flip.png")
    enemy_image_names = {"NINJA": "ninja.png", "OGRE": "ogre.png", "DEMON": "demon.png"}
    enemy_image_names_flipped = {"NINJA": "ninjaflip.png", "OGRE": "ogreflip.png", "DEMON": "demonflip.png"}

    buffer_width = 40

    '''
    🤺          👹
    (100,600)   (660, 600)
    '''

    start_x, start_y, curr_y, enemy_x, enemy_y, curr_enemy_y = 100, 600, 600, 700 - buffer_width, 600, 600
    ground_y = 600

    role_jump_t, enemy_jump_t = -1, -1

    role_rect, enemy_rect = None, None
    print(Setting := Setting.name.upper())

    '''
    Goal: To develop a reinforcement learning agent to learn the best moves at each step/iteration
    to maximize the probability of defeating the player.

    Step 1: Define a Reward Function (given at each time step (t = 0, 1, 2, ..., end)
        - Example 1:
            1       if the Role took damage
            0       if no one took damage
            -1      if the agent took damage
        - Example 2:
            1       if the Role took damage
            -0.5    if no one took damage (b/c the agent didn't hit the target)
            -1      if the agent took damage
        - Example 3:
            Reward = dd * (damage_dealt / role.base_health) - dt * (damage_taken / enemy.base_health)

            dt = (enemy.base_health - enemy.health) / enemy.base_health

                Example 1:
                    enemy.base_health = 100
                    enemy.health = 99
                    damage_taken = 1
                    -> second_term = .01 * 1 = .01

                Example 2:
                    enemy.base_health = 100
                    enemy.health = 19
                    damage_taken = 1
                    -> second_term = (100 - 19)/100 * 1 = 0.81

                Therefore, dt penalizes losing health more if the agent has less of it.

            dd = 1

    t = 0:
        Agent (agent_position = (660, 600), role_position = (0, 600), stats) -> choose between ("attack", "left", "right", "jump")

    MCTS
    ----
    N(s,a): Number of times the agent has taken an action a from the state s
    Q(s,a): Estimation of the expected reward of taking action a from the state s
         - Q(s,a) = max(Q(s,a), score)  if N(s,a) > 0
                    0                   if N(s,a) = 0


                E.g. piecewise function:
                    f(x) = x^2  if x > 0
                           -x   if x <= 0
    N(s): Number of times the agent has visited the state s

    Q: How do you choose actions?
    A: Using the upper-confidence tree (UCT) formula

        UCT = Q(s,a) + c*sqrt( ln(N(s)) / N(s,a) )

    where c is the regularization term -> hyperparameter -> controls the exploitation/exploitation tradeoff

    c = sqrt(2) is typical in literature, also 1 is common

    Q(s,a) <- max(Q(s,a), score)

    '''
    Qsa = {}
    Nsa = {}
    Ns = {}

    if os.path.isfile('Qsa.json') and os.path.isfile('Nsa.json') and os.path.isfile('Ns.json'):
        with open('Qsa.json') as json_file:
            Qsa = json.load(json_file)
        with open('Nsa.json') as json_file:
            Nsa = json.load(json_file)
        with open('Ns.json') as json_file:
            Ns = json.load(json_file)

    def save_stats():
        with open("Qsa.json", "w") as outfile:
            json.dump(Qsa, outfile)
        with open("Nsa.json", "w") as outfile:
            json.dump(Nsa, outfile)
        with open("Ns.json", "w") as outfile:
            json.dump(Ns, outfile)

    c = sqrt(2)
    #    State = namedtuple("State", "agent_x agent_y role_x role_y agent_health") #maybe include role_health as well?
    enemy_options = ("attack", "left", "right", "jump", "rest")
    max_score = -np.inf
    dd = 1

    def spawnBadNPC():
        '''
        Spawns a random oponent
        '''
        randnum = randint(1, 100)
        start = 1
        end = 0
        for b in badNPCs:
            end += int(b.second * 100)  # probability of spawning
            if start <= randnum <= end:
                enemy = BadNPC(cppStringConvert(b.first))  # we are spawning an enemy here
                enemy.statboost(role)
                return enemy

    enemies = [spawnBadNPC() for i in range(10)]
    enemy = enemies[0]
    getEnemyHealth = lambda: sum(i.health for i in enemies)
    getEnemyBaseHealth = lambda: sum(i.base_health for i in enemies)

    def renderRole(start_x, start_y):
        global font
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
        pygame_print(f"Quest #{role.questLevel + 1}", loc=60)
       
        # Role Health Bar Health Bar
        #min(Y) = 150, min(X) = 165, max(Y) = 252, max(X) = 335
        pygame.draw.rect(screen, white, (150, 137, 200, 120))
        font = pygame.font.Font('freesansbold.ttf', 22)
        pygame_print(cppStringConvert(role.name), loc = 150, offset=-150)
        font = pygame.font.Font('freesansbold.ttf', 20)
        pygame_print("Lv. = "+ str(role.currLevel), loc=175, offset=-115)
        font = pygame.font.Font('freesansbold.ttf', 22)
        pygame.draw.rect(screen, black, (165, 195, 150, 20)) #165 -> 165/800*X, 195 -> 195/750*Y
        pygame.draw.rect(screen, green, (165, 195, int(150*role.health/role.base_health), 20)) #Health bar
        font = pygame.font.Font('freesansbold.ttf', 20)
        pygame_print(f"{role.health:.0f} / {role.base_health:.0f}", loc=230, offset=-125)
        font = pygame.font.Font('freesansbold.ttf', 22)
        pygame.draw.rect(screen, black, (165, 242, 170, 10))
        pygame.draw.rect(screen, cyan, (165, 242, int(170*role.currExp/role.LevelExp), 10)) #Exp bar
        
        role_image = pygame.image.load(
            f"Assets/{role_image_name}" if not role.flipped else f"Assets/{role_image_name_flipped}")
        role_image = pygame.transform.scale(role_image, (buffer_width, buffer_width))
        screen.blit(role_image, role_rect.topleft)
        
        # Enemy Health Bar
        #min(Y) = 170, min(X) = 485, max(Y) = 230, max(X) = 635
        pygame.draw.rect(screen, white, (465, 140, 190, 120))

        pygame_print(cppStringConvert(enemy.name), loc = 170, offset=+150)
        pygame.draw.rect(screen, black, (485, 195, 150, 20))
        pygame.draw.rect(screen, red, (485, 195, int(150*enemy.health/enemy.base_health), 20)) #Health bar
        font = pygame.font.Font('freesansbold.ttf', 20)
        pygame_print(f"{enemy.health:.0f} / {enemy.base_health:.0f}", loc=230, offset=+187)
        font = pygame.font.Font('freesansbold.ttf', 22)
        
        enemy_image = pygame.image.load(
            f"Assets/{enemy_image_names[enemy.name]}" if not enemy.flipped else f"Assets/{enemy_image_names_flipped[enemy.name]}")
        enemy_image = pygame.transform.scale(enemy_image, (buffer_width, buffer_width))
        screen.blit(enemy_image, enemy_rect.topleft)
        font = pygame.font.Font('freesansbold.ttf', 32)

    role_rect = pygame.Rect(start_x, start_y, buffer_width, buffer_width)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, buffer_width, buffer_width)
    renderRole(start_x, start_y)

    shotsFired = deque([], maxlen=10)
    shotsEnemyFired = deque([], maxlen=10)
    K = 10  # Constant factor for gravity

    global badNPCs  # we're saying that we will be using the global variable badNPCs
    NumberDefeated = 0

    start_msg_time = time()
    start_msg_interval = 2  # At the beginning of each round, a message saying 'spawning new enemy' will appear for 2 seconds

    def generateMove(temp_state):
        '''
        Generate a move that the agent should make based on the UCT formula:
            UCT = Q(s,a) + c*sqrt( ln(N(s)) / N(s,a) )
        '''

        UCT = 0
        UCT_best = -np.inf
        best_act = "None"

        for enemy_option in enemy_options:
            # If the condition below is true then we can use the UCT formula
            if Nsa.get(temp_state) and int(Nsa[temp_state].get(enemy_option) or 0) > 0 and Qsa.get(temp_state) and Qsa.get(temp_state).get(enemy_option):
                UCT = Qsa[temp_state][enemy_option] + c * sqrt(ln(Ns[temp_state] / Nsa[temp_state][enemy_option]))
            else:
                UCT = np.inf  # encourage this action since it has no visit counts
            if UCT > UCT_best:
                best_act = enemy_option
                UCT_best = UCT

        if Ns.get(temp_state):
            Ns[temp_state] += 1
            if Nsa[temp_state].get(best_act):  # if the state-action pair has been visited before
                Nsa[temp_state][best_act] += 1
            else:  # if the state has been visited but the action has not been taken from this state yet
                Nsa[temp_state][best_act] = 1
        else:  # if the state-action pair has not been visited before
            Ns[temp_state] = 1
            Nsa[temp_state] = {}
            Nsa[temp_state][best_act] = 1

        return enemy_options.index(best_act)

    #        return randint(0, 3)

    n_iter = 0

    max_score = -np.inf
    check_point_score = -np.inf
    while True:  # pygame loop
        if n_iter != 0 and n_iter % 150 == 0:
            if check_point_score == max_score:
                c += sqrt(2)
            else:
                c = sqrt(2)
                check_point_score = max_score

        n_iter += 1
        last_role_health = role.health
        last_agent_health = getEnemyHealth()  # enemy.health
        temp_state = f"State(agent_x = {enemy_x:0.0f}, agent_y = {curr_enemy_y:0.0f}, role_x = {start_x:0.0f}, role_y = {curr_y:0.0f}, agent_health = {enemy.health:0.0f}, agent_flipped = {enemy.flipped})"
        enemyMove = generateMove(temp_state)
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_RETURN:
                    save_stats()
                    return
                elif event.key == pygame.K_SPACE:  # Checking if the role hero fired a shot
                    # Put beam on the screen if role has the stamina for it
                    if role.can_attack():
                        beam_x = start_x + (buffer_width if not role.flipped else 0)
                        beam_y = curr_y + buffer_width / 2
                        # Puts the coordinate of the shots fired on the screen
                        shotsFired.append(Shot(beam_x, beam_y, False,
                                               role.flipped))  # x-position of beam, y-position of beam, has it hit the target?, flipped?
                        # Update the wait-time here.
                        role.update_wait_time()

        if enemy_options[enemyMove] == "jump" and enemy_y + 200 >= ground_y:  # Holding down jump makes it bigger
            curr_enemy_y -= 5
            enemy_y = curr_enemy_y
            enemy_jump_t = time()
        if enemy_options[enemyMove] == "attack" and enemy.can_attack():
            beam_x = enemy_x + (0 if not enemy.flipped else buffer_width)
            beam_y = curr_enemy_y + buffer_width / 2
            # Puts the coordinate of the shots fired on the screen
            shotsEnemyFired.append(Shot(beam_x, beam_y, False,
                                        enemy.flipped))  # x-position of beam, y-position of beam, has it hit the target?, flipped?
            enemy.update_wait_time()

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
            if start_x < X - buffer_width:
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
            if enemy_x < X - buffer_width:
                enemy_x += enemy.speed * 10
            enemy.flipped = True
        if enemy_options[enemyMove] == "left":
            if enemy_x > 0:
                enemy_x -= enemy.speed * 10
            enemy.flipped = False

        role_rect = pygame.Rect(start_x, curr_y, buffer_width, buffer_width)
        enemy_rect = pygame.Rect(enemy_x, curr_enemy_y, buffer_width, buffer_width)
        renderRole(start_x, curr_y)

        for shot in shotsFired:
            shot.beam_x = shot.beam_x + 50 if not shot.is_flipped else shot.beam_x - 50  # TODO: make the shot speed depend on the role's stats?
            beam_rect = pygame.Rect(shot.beam_x, shot.beam_y, buffer_width / 2,
                                    buffer_width / 4)  # beam object
            if beam_rect.colliderect(
                    enemy_rect) and not shot.hit_target:  # Enemy was hit and this is not a repeat of the same shot
                role.attack(enemy)
                pygame.draw.rect(screen, red, enemy_rect, 2)
                if enemy.health == 0:
                    money += enemy.expYield*10
                    increaseExp(role, enemy.expYield)
                    NumberDefeated += 1
                    renderRole(start_x, curr_y)
                    if NumberDefeated < 10:
                        enemy = enemies[NumberDefeated]  # spawnBadNPC()
                        #                        last_agent_health = enemy.health
                        pygame_print(f"Spawning enemy #{NumberDefeated + 1}/10: {enemy.name}", loc=300)
                        start_msg_time = time()
                    else:
                        role.questLevel += 1
                        role.money += money
                        pygame_print(f"You Won!!", loc=300)

                shot.hit_target = True
            pygame.draw.ellipse(screen, orange, beam_rect)  # Drawing the beam

        for shot in shotsEnemyFired:
            shot.beam_x = shot.beam_x - 50 if not shot.is_flipped else shot.beam_x + 50
            beam_rect = pygame.Rect(shot.beam_x, shot.beam_y, buffer_width / 2, buffer_width / 4)  # beam object
            if beam_rect.colliderect(
                    role_rect) and not shot.hit_target:  # Role was hit and this is not a repeat of the same shot
                enemy.attack(role)
                pygame.draw.rect(screen, red, role_rect, 2)

                shot.hit_target = True
            pygame.draw.ellipse(screen, red, beam_rect)  # Drawing the beam

        if role.health <= 0:
            pygame_print("You died!", loc=300)
        elif time() - start_msg_time < start_msg_interval and NumberDefeated < 10:
            pygame_print(f"Spawning enemy #{NumberDefeated + 1}/10: {enemy.name}", loc=300)

        pygame.display.update()

        if NumberDefeated == 10 or role.health <= 0:
            # Do stuff
            pygame.time.delay(1000)
            pygame.event.clear(eventtype=pygame.KEYDOWN)
            save_stats()
            return

        '''
        Reward = dd * (damage_dealt / role.base_health) - dt * (damage_taken / enemy.base_health)

        dt = (enemy.base_health - enemy.health) / enemy.base_health
        dd = 1
        '''

        damage_dealt = last_role_health - role.health
        damage_taken = last_agent_health - getEnemyHealth()  # enemy.health
        dt = (getEnemyBaseHealth() - getEnemyHealth()) / getEnemyBaseHealth()
        score = dd * (damage_dealt / role.base_health) - dt * (damage_taken / getEnemyBaseHealth())

        if score > max_score:
            max_score = score

        if Qsa.get(temp_state):
            if Qsa[temp_state].get(enemy_options[enemyMove]):  # if the state-action pair has been visited before
                Qsa[temp_state][enemy_options[enemyMove]] = max(Qsa[temp_state][enemy_options[enemyMove]], score)
            else:  # if the state has been visited but the action has not been taken from this state yet
                Qsa[temp_state][enemy_options[enemyMove]] = score
        else:  # if the state-action pair has not been visited before
            Qsa[temp_state] = {}
            Qsa[temp_state][enemy_options[enemyMove]] = score

        '''
        What we have to store for continual learning:
         - Qsa, Nsa, Psa:
            * NN: stores the weights and biases of the Neural Network
            * SA: stores the dictionary of all visited state action pairs

        '''

def SellOption(Role):
    if not HasSellableItems(Role.numInv):
        pygame_print("You don't have any sellable items!", 300, color=black, background_color=white)
        pygame.display.update()
        pygame.time.delay(1000)
        pygame.event.clear(eventtype=pygame.KEYDOWN)
        return
    
    sellableItems = Role.printSellItemsVec(False, False)
    
    optionNumber = 0
    maxItems = 3
    startSellIdx = 0
    endSellIdx = min(sellableItems.size(), maxItems)
    while True:
        screen.fill(white)  # clear the screen
        pygame_print(f"What would you like to sell today?", 60, color=black, background_color=white)
        pygame_print("=================================", 100, color=black, background_color=white)
        text_y = 140
        for i in range(startSellIdx, endSellIdx):
            pygame_print(sellableItems[i].title(), text_y, color=(orange if optionNumber == i else black), background_color=white)
            text_y += 40

        pygame_print(f"Your Money = {Role.money:0.2f}", text_y + 20, color=black, background_color=white)

        stop_button = AddButton(text="EXIT", offset=0, loc=text_y + 80, background_color=red)

        pygame.display.update()
        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != sellableItems.size() - 1 else 0
                    if optionNumber == 0:
                        startSellIdx = 0
                    elif startSellIdx + 1 + maxItems <= sellableItems.size() and optionNumber > startSellIdx - 1 + maxItems:
                        startSellIdx += 1
                    
                    endSellIdx = startSellIdx + min(sellableItems.size(), maxItems)
                                       
                    '''
                e.g. maxItems = 3,
                start: startSellIdx = 0, startSellIdx = 3
                    
                0.    Water
                1.    Apple
                2.    Tomato
                3.    Melon
                4.    Orange
                5.    Pinapple
                6.    Grapefruit
                7.    Blueberry
                8.    Strawberry
                9.    Tootsie Roll
                    '''
                    
                elif event.key == pygame.K_UP:
                    optionNumber = optionNumber - 1 if optionNumber != 0 else sellableItems.size() - 1

                    if optionNumber < startSellIdx:
                        startSellIdx = startSellIdx - 1 if startSellIdx - 1 >= 0 else 0
                    elif optionNumber > startSellIdx + maxItems - 1:
                        startSellIdx = optionNumber - maxItems + 1
                    
                    endSellIdx = startSellIdx + min(sellableItems.size(), maxItems)
                    
                elif event.key == pygame.K_RETURN:
                    sellItem(Role, sellableItems[optionNumber].title())
                    sellableItems = Role.printSellItemsVec(False, False)
                    if sellableItems.size() == 0:
                        return
                    
                    optionNumber = 0
                    startSellIdx = 0
                    endSellIdx = min(sellableItems.size(), maxItems)
                    screen.fill(white)
                elif rect.collidepoint(pygame.mouse.get_pos()):
                    rect = AddButton(text="Buy", offset=200, loc=630, background_color=orange)
                    pygame.display.update()
                elif not rect.collidepoint(pygame.mouse.get_pos()):
                    rect = AddButton(text="Buy", offset=200, loc=630, background_color=green)
                    pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return


def BuyOption(Role):
    if Role.money == 0:
        pygame_print("You don't have any money!", 300, color=black, background_color=white)
        pygame.display.update()
        pygame.time.delay(1000)
        pygame.event.clear(eventtype=pygame.KEYDOWN)
        return

    buyableItems = Role.printBuyItemsVec(False)
    if buyableItems.size() == 0:
        pygame_print("You don't have enough money and/or", 300, color=black, background_color=white)
        pygame_print("you haven't completed enough quests!", 340, color=black, background_color=white)
        pygame.display.update()
        pygame.time.delay(1000)
        pygame.event.clear(eventtype=pygame.KEYDOWN)
        return

    optionNumber = 0
    maxItems = 3
    startBuyIdx = 0
    endBuyIdx = min(buyableItems.size(), maxItems)
    
    while True:
        screen.fill(white)  # clear the screen
        pygame_print(f"What would you like to buy today?", 60, color=black, background_color=white)
        pygame_print("=================================", 100, color=black, background_color=white)
        text_y = 140
        for i in range(startBuyIdx, endBuyIdx):
            pygame_print(buyableItems[i].title(), text_y, color=(orange if optionNumber == i else black), background_color=white)
            text_y += 40

        pygame_print(f"Your Money = {Role.money:0.2f}", text_y + 20, color=black, background_color=white)

        stop_button = AddButton(text="EXIT", offset=0, loc=text_y + 80, background_color=red)

        pygame.display.update()
        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != buyableItems.size() - 1 else 0
                    if optionNumber == 0:
                        startBuyIdx = 0
                    elif startBuyIdx + 1 + maxItems <= buyableItems.size() and optionNumber > startBuyIdx - 1 + maxItems:
                        startBuyIdx += 1
                    
                    endBuyIdx = startBuyIdx + min(buyableItems.size(), maxItems)
                                       
                    '''
                e.g. maxItems = 3,
                start: startBuyIdx = 0, endBuyIdx = 3
                    
                0.    Water
                1.    Apple
                2.    Tomato
                3.    Melon
                4.    Orange
                5.    Pinapple
                6.    Grapefruit
                7.    Blueberry
                8.    Strawberry
                9.    Tootsie Roll
                    '''
                    
                elif event.key == pygame.K_UP:
                    optionNumber = optionNumber - 1 if optionNumber != 0 else buyableItems.size() - 1

                    if optionNumber < startBuyIdx:
                        startBuyIdx = startBuyIdx - 1 if startBuyIdx - 1 >= 0 else 0
                    elif optionNumber > startBuyIdx + maxItems - 1:
                        startBuyIdx = optionNumber - maxItems + 1
                    
                    endBuyIdx = startBuyIdx + min(buyableItems.size(), maxItems)
                    
                elif event.key == pygame.K_RETURN:
                    buyItem(Role, buyableItems[optionNumber].title())
                    buyableItems = Role.printBuyItemsVec(False)
                    if buyableItems.size() == 0:
                        return
                    
                    optionNumber = 0
                    startBuyIdx = 0
                    endBuyIdx = min(buyableItems.size(), maxItems)
                    screen.fill(white)
            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return


def Shop(Role):
    optionNumber = 0
    Role.money = 1e6 #TODO: delete
    while True:
        screen.fill(white)  # clear the screen
        pygame_print("What would you like to do today?", 90, color=black, background_color=white)
        pygame_print("================================", 130, color=black, background_color=white)
        pygame_print("Buy", 170, color=(orange if optionNumber == 0 else black), background_color=white)
        pygame_print("Sell", 210, color=(orange if optionNumber == 1 else black), background_color=white)

        stop_button = AddButton(text="EXIT", offset=0, loc=310, background_color=red)

        pygame.display.update()
        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != 1 else 0
                elif event.key == pygame.K_UP:
                    optionNumber = optionNumber - 1 if optionNumber != 0 else 1
                elif event.key == pygame.K_RETURN:
                    screen.fill(white)
                    if optionNumber == 0:  # Buy
                        BuyOption(Role)
                    elif optionNumber == 1:  # Sell
                        SellOption(Role)
                    pygame.display.update()
                    pygame.event.clear(eventtype=pygame.KEYDOWN)

            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
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
                            Shop(role)
                        elif optionNumber == 5:  # Quests
                            QuestGames(setting, role)
                        elif optionNumber == 6:  # Stats
                            Stats(role)
                        return

def game():
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
