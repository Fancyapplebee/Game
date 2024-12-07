from string import punctuation
import json
import os
from math import sqrt, log as ln
from random import random, randint
from string import punctuation
from time import time
import cppyy
import numpy as np
import pygame
from PIL import Image
from copy import deepcopy

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
# Add use function for each of the items ✅
# Boost stats of hero after a quest, and maybe also after mining? ✅
# quest2 -> In C programming
# Work on menu option function where you can use some of your items to build weapons that can boost your stats 👨‍💻
# figure out use case of items not attainable through mining
# implement a save function
# saving => writes information to a file (e.g. time, stats, items, time that the RoleHero last searched etc.)
# modify search option so that it can only occur once per people day ✅
# Axes that can increase drop-chances for mine function
# Find out where we can increase money besides selling ✅
# Figure out if holding the up/down arrow keys can make it continue going up/down in the menu parts of the game.
# if event.type -> elif event.type in `for event in pygame.event.get()`

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
    struct Shot
    {
        double beam_x, beam_y;
        bool hit_target, is_flipped, is_special_shot;
        std::string special_image;
        
        Shot(double beam_x, double beam_y, bool hit_target, bool is_flipped, bool is_special_shot = false, std::string special_image = "")
        {
            this->beam_x = beam_x;
            this->beam_y = beam_y;
            this->hit_target = hit_target;
            this->is_flipped = is_flipped;
            this->is_special_shot = is_special_shot;
            this->special_image = special_image;
        }
    };
    
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
    
    struct SpecialShot
    {
        std::string specialShotImage;
        std::string specialShotType;
        bool isSpecialShot;
    };

    struct BadNPC : public SpecialShot
    {
        const std::string name;
        std::string picture;
        double shot_speed;
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
            this->shot_speed = 5; //TODO: change based on BADNPC, also maybe the size/color/shape of the shot?
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
            this->shot_speed = 5;
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
            this->shot_speed = 5;
            this->attackpower = 10;
            this->base_health = 100.0;
            this->health = 100.0;
            this->defense = 20;
            this->expYield = 5;
            this->speed = 1.25;
            this->attackStamina = 0.9;
        }
    }


    struct Role : public SpecialShot
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
        std::unordered_map<std::string, double> specialShotMultipliers;

        double health;
        double base_health;
        double shot_speed;
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
        void attack(BadNPC& enemy, double multiplier = 1.0);
        void baseLineStats();
        std::vector<std::string> printInventory();
        std::unordered_map<std::string, double> printSellItems(bool print = false);
        std::vector<std::string> printSellItemsVec(bool print = false, bool upper = true);
        std::vector<std::string> getTradableItems();
        std::unordered_map<std::string, double> printBuyItems(bool print = true);
        std::vector<std::string> printBuyItemsVec(bool print = true);
        std::vector<std::string> QuestItemsVec();
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

    void Role::attack(BadNPC& enemy, double multiplier)
    {
        enemy.health -= (Defense(enemy.defense) * attackpower * multiplier); //the enemy's health can go below 0, so see below :)
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
        shot_speed = multiplier * shot_speed;
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
    
    std::vector<std::string> Role::QuestItemsVec()
    {
        std::vector<std::string> questItems;
        
        for (auto& i: stringInv)
        {
            //if (numInv[i.first].find("QuestLevel") != numInv[i.first].end())
            //{
            questItems.push_back(i.first);
            //}
        }
        
        return questItems;
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
        shot_speed = 0;
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

    /*
    InputMap:
    
    Idea: Intially empty
    
        Keys of InputMap: strings denoting keys on the keyboard
        Values of InputMap: The item that the given key on the keyboard maps to
    
    User Interface:
    
        1. Select an item
        2. Select the key(s) that you want to map to this item
        
        3. for key in key_selected: InputMap[key] = item
    
    QuestGames:
        We need to check if a key in the current InputMap was selected.
            -> We need a constant dictionary (say, pygameKeys) routing every possible key on a standard keyboard to the corresponding pygame.KEYDOWN event
        
        E.g. for key in InputMap: if event.key == pygameKeys[key] -> use(InputMap[key])
    
    */
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
                                        this->isSpecialShot = false;
                                        if (numInv["Cookies"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        numInv["Cookies"]["Number"]--;
                                        health += 0.1*health;
                                        if (health > base_health)
                                        {
                                            health = base_health;
                                        }
                                   }
                           }}
            },

            {
                "Logs",{{"Use",
                                    [&]()
                                    {
                                        this->isSpecialShot = true;
                                        if (numInv["Logs"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Logs"]["Picture"];
                                        numInv["Logs"]["Number"]--;
                                    }
                           }}
            },

            {
                "Key 1",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = false;
                                        if (numInv["Key 1"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        numInv["Key 1"]["Number"]--;
                                   }
                           }}
            },

            {
                "Sands",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Sands"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Sands"]["Picture"];
                                        numInv["Sands"]["Number"]--;
                                   }
                           }}
            },

            {
                "Rocks",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Rocks"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        numInv["Rocks"]["Number"]--;
                                        this->specialShotImage = this->stringInv["Rocks"]["Picture"];
                                        //std::cout << this->specialShotImage << '\n';
                                   }
                           }}
            },

            {
                "Silvers",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Silvers"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Silvers"]["Picture"];
                                        numInv["Silvers"]["Number"]--;
                                   }
                           }}
            },

            {
                "Golds",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Golds"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Golds"]["Picture"];
                                        numInv["Golds"]["Number"]--;
                                   }
                           }}
            },

            {
                "Diamonds",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Diamonds"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Diamonds"]["Picture"];
                                        numInv["Diamonds"]["Number"]--;
                                   }
                           }}
            },

            {
                "Emeralds",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Emeralds"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Emeralds"]["Picture"];
                                        numInv["Emeralds"]["Number"]--;
                                   }
                           }}
            },

            {
                "Cactuses",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Cactuses"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Cactuses"]["Picture"];
                                        numInv["Cactuses"]["Number"]--;
                                   }
                           }}
            },

            {
                "Golden Saplings",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Golden Saplings"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Golden Saplings"]["Picture"];
                                        numInv["Golden Saplings"]["Number"]--;
                                   }
                           }}
            },

            {
                "Golden Logs",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Golden Logs"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Golden Logs"]["Picture"];
                                        numInv["Golden Logs"]["Number"]--;
                                   }
                           }}
            },

            {
                "Sand Pails",{{"Use",
                                   [&]()
                                   {
                                        this->isSpecialShot = true;
                                        if (numInv["Sand Pails"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Sand Pails"]["Picture"];
                                        numInv["Sand Pails"]["Number"]--;
                                   }
                           }}
            },

            {
                "Potion",{{"Use",
                                   [&]()
                                   {
                                       this->isSpecialShot = false;
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
                                       this->isSpecialShot = false;
                                       if (numInv["Apple"]["Number"] == 0)
                                       {
                                            return;
                                       }
                                       numInv["Apple"]["Number"]--;
                                       health += 0.25*health;
                                       if (this->health > base_health)
                                       {
                                           health = base_health;
                                       }
                                   }
                           }}
            },

            {
                "Knife",{{"Use",
                                    [&]()
                                    {
                                        this->isSpecialShot = true;
                                        if (numInv["Knife"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Knife"]["Picture"];
                                        numInv["Knife"]["Number"]--;
                                    }
                        }}
            },

            {
                "Parrot",{{"Use",
                                    [&]()
                                    {
                                        this->isSpecialShot = true;
                                        if (numInv["Parrot"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Parrot"]["Picture"];
                                        numInv["Parrot"]["Number"]--;
                                    }
                        }}
            },

            {
                "Ring",{{"Use",
                                    [&]()
                                    {
                                        this->isSpecialShot = true;
                                        if (numInv["Ring"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Ring"]["Picture"];
                                        numInv["Ring"]["Number"]--;
                                    }
                        }}
            },

            {
                "Cape",{{"Use",
                                    [&]()
                                    {
                                        this->isSpecialShot = false;
                                        if (numInv["Cape"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        numInv["Cape"]["Number"]--;
                                    }
                        }}
            },

            {
                "Armor",{{"Use",
                                    [&]()
                                    {
                                        this->isSpecialShot = false;
                                        if (numInv["Armor"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        numInv["Armor"]["Number"]--;
                                    }
                        }}
            },

            {
                "Water Guns",{{"Use",
                                    [&]()
                                    {
                                        this->isSpecialShot = true;
                                        if (numInv["Water Guns"]["Number"] == 0)
                                        {
                                            return;
                                        }
                                        this->specialShotImage = this->stringInv["Water Guns"]["Picture"];
                                        numInv["Water Guns"]["Number"]--;
                                    }
                        }}
            }
        };
        
        this->specialShotMultipliers = {{"Assets/parrot.png", 2.36024}, {"Assets/knife.png", 2.46055}, {"Assets/sapling.png", 2.22583}, {"Assets/cactus.png", 2.38649}, {"Assets/diamond.png", 2.23146}, {"Assets/gold.png", 2.06248}, {"Assets/water gun.png", 2.2429}, {"Assets/Sand Pail.png", 2.43646}, {"Assets/rock.png", 2.41957}, {"Assets/Golden Log.png", 2.17529}, {"Assets/emerald.png", 2.18229}, {"Assets/sand.png", 2.30797}, {"Assets/silver.png", 2.47529}, {"Assets/log.png", 2.37766}, {"Assets/ring.png", 2.12051}};
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
from cppyy.gbl import Role, BadNPC, badNPCs, HasSellableItems, Shot

# Takes in a C++ string, and returns a correct python string
def cppStringConvert(string):
    temp = ""
    for i in range(string.length()):
        temp = temp + string[i]
    return temp  # a python string

class IPBase:
    def __init__(self):
        self.InputMapDict = {}
        self.InputMapDictKeys = []

class PercyJackson(Role, IPBase):
    def __init__(self, name):
        Role.__init__(self, name)
        IPBase.__init__(self)
        self.picture = "⚡️"
        self.image_name = "percy-start.png"
        self.shot_speed = 15
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

class Elf(Role, IPBase):
    def __init__(self, name):
        Role.__init__(self, name)
        IPBase.__init__(self)
        self.picture = "🧝"
        self.image_name = "elf-start.png"
        self.shot_speed = 10
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


class Zelda(Role, IPBase):
    def __init__(self, name):
        Role.__init__(self, name)
        IPBase.__init__(self)
        self.picture = "🗡"
        self.image_name = "zelda-start.png"
        # TODO: Change back to 20 for actual game
        self.attackpower = 2000
        self.shot_speed = 15
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
        self.role = neutralNPCs[randint(0, len(neutralNPCs) - 1)].title()
        if self.role == "Miner":
            self.picture = "⛏"
            self.expYield = 0.1 + random() / 20  # random number from 0.1 - 0.15
            self.image_name = "miner.png"
        elif self.role == "Woodchucker":
            self.picture = "🪓"
            self.expYield = 0.12 + random() / 50  # random number from 0.12 - 0.14
            self.image_name = "woodchucker.png"


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
base_screen_height = Y
def scale_font(size):
    global base_screen_height
    scale_factor = Y / base_screen_height
    return int(size * scale_factor)

# Example of using this function to create fonts
base_font_size = 32  # Base font size you designed for
font_size = base_font_size
#scaled_font_size = scale_font(font_size)
font = pygame.font.Font('freesansbold.ttf', scale_font(font_size))
#print(scaled_font_size)
base_font_height = font.size("hi")[1]

def pygame_print(text, loc_y=Y // 2, color=black, background_color=white, offset_x=0, scale = True, thresh = 0.9):
    global X, Y, font, font_size, base_screen_height, base_font_height, base_font_size
    font_size = base_font_size
    font = pygame.font.Font('freesansbold.ttf', font_size)
    #Rescaling the font size so it does not trail off the screen
    threshold = thresh*X
    scaled_font_height = (Y*base_font_height)/base_screen_height
    
    font_sz = font.size(text)
    while font_size > 1 and (font_sz[0] > threshold or font_sz[1] > scaled_font_height):
        font_size -= 1
        font = pygame.font.Font('freesansbold.ttf', font_size)
        font_sz = font.size(text)
        
    
    
    font = pygame.font.Font('freesansbold.ttf', font_size)
    
    
    text = font.render(text, True, color, background_color)
    textRect = text.get_rect()
    textRect.center = (X//2+offset_x, loc_y)
    screen.blit(text, textRect)
    
    # Adjust fonts dynamically based on screen size
    return textRect
    
screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
#old_screen = screen
#while True:
#    pygame.event.pump()
#    event = pygame.event.wait()
#    if event.type == pygame.QUIT: pygame.display.quit()
#    elif event.type == pygame.VIDEORESIZE:
#        width, height = event.size
#        if width < 400:
#            width = 400
#        if height < 300:
#            height = 300
#        screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
def wait_til_enter():
    global X, Y, screen
    while True:
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
#                if event.key == pygame.K_RETURN:
#                pygame.event.clear(eventtype=pygame.KEYDOWN)
                return False #Not resized
            elif event.type == pygame.VIDEORESIZE:
                #old_screen = screen
#                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                print(f"X, Y = {X}, {Y}")
                return True #Resized
                #                    screen.blit(old_screen, (0,0))
#                pygame.display.update()

#def pygame_print(text, loc_y=Y // 2, color=black, background_color=white, offset_x=0):
#    text = font.render(text, True, color, background_color)
#    textRect = text.get_rect()
#    textRect.center = (X // 2 + offset_x, loc_y)
#    screen.blit(text, textRect)
#    return textRect

#def updateList(items: list, selectNumber: int, color: tuple = light_pink, inc: int = int(0.053*Y), height: float = 4,
#               new_screen=True) -> None:
def updateList(items: list, selectNumber: int, color: tuple = light_pink, inc: int = int(0.1*Y), height: float = 4,
               new_screen=True) -> None:
    global screen, old_screen, X, Y
    count = 0
    if new_screen:
        screen.fill(color)
    for num, item in enumerate(items):
        pygame_print(item, Y // height + count, color=(yellow if num == selectNumber else black),
                     background_color=color)
        count += inc
    print("called updateList")
    pygame.display.update()
    #old_screen = screen

# all images are in Game/Game/Assets
def displayImage(rsp, height: bool = False, p: int = 0, update: bool = True):
    global screen
    rsp = os.getcwd() + "/Assets/" + rsp
    pilimage = Image.open(rsp).convert("RGBA")
    if p == 0:
        pilimage = pilimage.resize((int(0.4375*X), int(0.467*Y)))
    elif p == 1:
        pilimage = pilimage.resize((int(X), int(Y)))
    pgimg = pygame.image.fromstring(pilimage.tobytes(), pilimage.size, pilimage.mode)
    if not height:
        height = (int(0.167*Y) - pgimg.get_rect().height) / 8

    screen.fill(white)
    screen.blit(pgimg, ((X - pgimg.get_rect().width) // 2, height))
    if update:
        pygame.display.update()

def displayImageCustom(rsp, width, height, loc_x, loc_y):
    global screen
    rsp = os.getcwd() + "/Assets/" + rsp
    pilimage = Image.open(rsp).convert("RGBA")
    pilimage = pilimage.resize(((width), (height)))
    pgimg = pygame.image.fromstring(pilimage.tobytes(), pilimage.size, pilimage.mode)
    screen.blit(pgimg, (loc_x, loc_y))

def openChestOption(optionNumber=None):
    pygame_print("Yes", Y // 1.5 + int(0.11*Y), color=(orange if optionNumber == 0 else black))
    pygame_print("No", Y // 1.5 + int(0.22*Y), color=(orange if optionNumber == 1 else black))
    pygame.display.update()


def PlaceOption(optionNumber=None):
    pygame_print("House", int(0.2*Y), color=(orange if optionNumber == 0 else black))
    pygame_print("Beach", int(0.2534*Y), color=(orange if optionNumber == 1 else black))
    pygame_print("Forest", int(0.3067*Y), color=(orange if optionNumber == 2 else black))
    pygame_print("Mountain", int(0.36*Y), color=(orange if optionNumber == 3 else black))
    pygame_print("Desert", int(0.413*Y), color=(orange if optionNumber == 4 else black))
    pygame.display.update()


# Setting Types
class Setting:
    def map(self):
        global font, white, black, X, Y, screen

        screen.fill(white)
        pygame_print("--------", int(0.12*Y))
        pygame_print("Places", int(0.1734*Y))
        pygame_print("--------", int(0.2267*Y))

        currHeight = int(0.28*Y)
        font = pygame.font.Font('freesansbold.ttf', int(0.03734*Y))
        for place in self.places:
            pygame_print(place.title(), currHeight)
            currHeight += int(0.0534*Y)
        font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
        pygame.display.update()
        while True:
            for event in pygame.event.get():  # update the option number if necessary
                if event.type == pygame.VIDEORESIZE:
                    X, Y = screen.get_width(), screen.get_height()
                    X = 410 if X < 410 else X
                    print(f"X, Y = {X}, {Y}")
                    screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                    screen.fill(white)
                    pygame_print("--------", int(0.12*Y))
                    pygame_print("Places", int(0.1734*Y))
                    pygame_print("--------", int(0.2267*Y))

                    currHeight = int(0.28*Y)
                    font = pygame.font.Font('freesansbold.ttf', int(0.03734*Y))
                    for place in self.places:
                        pygame_print(place.title(), currHeight)
                        currHeight += int(0.0534*Y)
                    font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
                    pygame.display.update()
                elif event.type == pygame.KEYDOWN:  # checking if any key was selected
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

#5 seconds * 1 hour  = (5 / 3600) * 1 hour = 5/3600 hours
#            ======
#            3600 seconds

def search(setting, role):
    global screen, X, Y
    currentTime = time()
    if currentTime - role.searchTime < 86400:
        while True:
            screen.fill(white)
            currentTime = time()
            time_til_search = (86400 - (currentTime - role.searchTime))
            hours = time_til_search // 3600
            remainder = time_til_search % 3600
            minutes = remainder // 60
            seconds = remainder % 60
            messages = ("Sorry, you cannot", "search at this point!", "Time until you can", "search again = ", f"{hours:.0f}:{minutes:.0f}:{seconds:.0f}")
            count = int(0.12*Y)
            for message in messages:
                pygame_print(message, count)
                count += int(0.067*Y)

            pygame.display.update()
            
            for event in pygame.event.get():  # update the option number if necessary
                if event.type == pygame.VIDEORESIZE:
                    X, Y = screen.get_width(), screen.get_height()
                    X = 410 if X < 410 else X
                    print(f"X, Y = {X}, {Y}")
                    screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:  # checking if any key was selected
                    if event.key == pygame.K_RETURN:
#                        pygame.event.clear(eventtype=pygame.KEYDOWN)
                        return

    optionNumber = 0
    numOptions = len(setting.places)
    breakFlag = False
    while True:
        screen.fill(white)  # clear the screen

        currHeight = int(0.12*Y)
        Question = f"Where in the {setting.name} do you want to explore?"
        pygame_print(Question[0:Question.index("do") - 1], currHeight)
        currHeight += int(0.0534*Y)
        pygame_print(Question[Question.index("do"):], currHeight)
        currHeight += int(0.08*Y)
        pygame_print("------", currHeight)
        currHeight += int(0.0534*Y)
        pygame_print("Places", currHeight)
        currHeight += int(0.0534*Y)
        pygame_print("------", currHeight)

        currHeight += int(0.0534*Y)
        currentOption = 0
        for place in setting.places:
            pygame_print(place.title(), currHeight, orange) if optionNumber == currentOption else pygame_print(
                place.title(), currHeight)
            currHeight += int(0.0534*Y)
            currentOption += 1
        pygame_print("------", currHeight)
        pygame.display.update()

        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
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
        displayImage("sand.png", p=0)
        pygame_print("You got SAND!", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()
        screen.fill(white)
        if Chances == 1:
            role.numInv["Sand Pails"]["Number"] += 1
            screen.fill(white)  # clear the screen
            displayImage("sand-pail.png", p=0)
            pygame_print("You got a Sand Pail!", int(0.267*Y))
            pygame.display.update()
            #pygame.time.delay(1000)  # waiting one second
            wait_til_enter()

    elif setting.places[optionNumber] == "HILLSIDE":
        Chances = randint(1, 1000)
        role.numInv["Sands"]["Number"] += 1
        displayImage("hillside.png", p=0)
        pygame_print("You got SAND!", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()
        screen.fill(white)
        if Chances == 1:
            role.numInv["Cactuses"]["Number"] += 1
            screen.fill(white)  # clear the screen
            displayImage("cactus.png", p=0)
            pygame_print("You found a cactus!", int(0.267*Y))
            pygame.display.update()
            #pygame.time.delay(1000)  # waiting one second
            wait_til_enter()

    elif setting.places[optionNumber] == "CASTLE":
        Chances = randint(1, 1e8)
        if Chances == 1:
            role.numInv["Golden Logs"] += 1
            displayImage("Golden log.png", p=0)
            pygame_print("SUPER RARE DROP: Golden Log!", int(0.267*Y))
        elif 2 <= Chances <= 11:
            role.numInv["Emeralds"]["Number"] += 1
            displayImage("emerald.png", p=0)
            pygame_print("You got an emerald.", int(0.267*Y))
        else:
            pygame_print("Nothing found.", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()

    elif setting.places[optionNumber] == "OCEAN":
        Chances = randint(1, 1e5)
        if Chances == 1:
            role.numInv["Golds"]["Number"] += 1
            displayImage("gold.png", p=0)
            pygame_print("You got gold!", int(0.267*Y))
        else:
            pygame_print("Nothing found.", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()

    elif setting.places[optionNumber] == "FRIDGE":
        Chances = randint(1, 1000)
        if 1 <= Chances <= 5:
            role.numInv["Cookies"]["Number"] += 1
            displayImage("cookie.png", p=0)
            pygame_print("You got a cookie!", int(0.267*Y))
        else:
            pygame_print("Nothing found.", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()

    elif setting.places[optionNumber] == "TREE":
        Chances = randint(1, 1000)
        if 1 <= Chances <= 5:
            role.numInv["Apple"]["Number"] += 1
            displayImage("apple.png", p=0)
            pygame_print("You got an apple!", int(0.267*Y))
        else:
            pygame_print("Nothing found.", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()

    elif setting.places[optionNumber] == "CAVE":
        Chances = randint(1, 10000)
        if Chances == 1:
            role.numInv["Silvers"]["Number"] += 1
            displayImage("silver.png", p=0)
            pygame_print("You got a piece of silver!", int(0.267*Y))
        elif 2 <= Chances <= 101:
            role.numInv["Rocks"]["Number"] += 1
            displayImage("rock.png", p=0)
            pygame_print("You got a rock!", int(0.267*Y))
        else:
            pygame_print("Nothing found.", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()

    #    100000/10 = 10000 -> 1e5/10 = 1e4
    #   1/100 = 10/1000 = 100/10000 = 1000/100000
    elif setting.places[optionNumber] == "TOP":
        Chances = randint(1, 1e5)
        if Chances == 1:
            role.numInv["Golds"]["Number"] += 1
            displayImage("gold.png", p=0)
            pygame_print("You got a piece of gold!", int(0.267*Y))
        elif 2 <= Chances <= 11:
            role.numInv["Silvers"]["Number"] += 1
            displayImage("silver.png", p=0)
            pygame_print("You got a piece of silver!", int(0.267*Y))

        elif 12 <= Chances <= 1011:
            role.numInv["Rocks"]["Number"] += 1
            displayImage("rock.png", p=0)
            pygame_print("You got a rock!", int(0.267*Y))
        else:
            pygame_print("Nothing found.", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()


    elif setting.places[optionNumber] == "LANDSCAPE":
        Chances = randint(1, 100000)
        role.numInv["Sands"]["Number"] += 1
        displayImage("sand.png", p=0)
        pygame_print("You got SAND!", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()
        screen.fill(white)
        if Chances == 1:
            role.numInv["Sand Pails"]["Number"] += 1
            displayImage("sand pail.png", p=0)
            pygame_print("You found a sand pail!", int(0.267*Y))
        elif 2 <= Chances <= 11:
            role.numInv["Cactuses"]["Number"] += 1
            displayImage("cactus.png", p=0)
            pygame_print("You found a cactus!", int(0.267*Y), 0)
        else:
            pygame_print("Nothing else found.", int(0.267*Y))
        pygame.display.update()
        #pygame.time.delay(1000)  # waiting one second
        wait_til_enter()

    role.searchTime = time()
    return setting.places[optionNumber]


def Stats(RoleHero):
    global X, Y, screen
    screen.fill(white)
    pygame_print(f"Attack Power = {RoleHero.attackpower:.0f}", int(0.12*Y))
    pygame_print(f"Health = {RoleHero.health:.0f} / {RoleHero.base_health:.0f}", int(0.1734*Y))
    pygame_print(f"Defense = {RoleHero.defense:.0f} / {RoleHero.baseDefense:.0f}", int(0.2267*Y))
    pygame_print(f"Speed = {RoleHero.speed:.2f}", int(0.28*Y))
    pygame_print(f"Attack Stamina = {RoleHero.attackStamina:.2f}", int(0.3333*Y))
    pygame_print(f"Defense Stamina = {RoleHero.defenseStamina:.2f}", int(0.3867*Y))
    pygame_print(f"Money = {RoleHero.money}", int(0.44*Y))
    pygame_print(f"Quest Level = {RoleHero.questLevel}", int(0.4933*Y))
    pygame_print(f"Stat Level = {RoleHero.currLevel:.0f}", int(0.5467*Y))
    pygame_print(f"Exp = {RoleHero.currExp:.2f} / {RoleHero.LevelExp:.2f}", int(0.6*Y))
    pygame.display.update()
    while True:
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)
                pygame_print(f"Attack Power = {RoleHero.attackpower:.0f}", int(0.12*Y))
                pygame_print(f"Health = {RoleHero.health:.0f} / {RoleHero.base_health:.0f}", int(0.1734*Y))
                pygame_print(f"Defense = {RoleHero.defense:.0f} / {RoleHero.baseDefense:.0f}", int(0.2267*Y))
                pygame_print(f"Speed = {RoleHero.speed:.2f}", int(0.28*Y))
                pygame_print(f"Attack Stamina = {RoleHero.attackStamina:.2f}", int(0.3333*Y))
                pygame_print(f"Defense Stamina = {RoleHero.defenseStamina:.2f}", int(0.3867*Y))
                pygame_print(f"Money = {RoleHero.money}", int(0.44*Y))
                pygame_print(f"Quest Level = {RoleHero.questLevel}", int(0.4933*Y))
                pygame_print(f"Stat Level = {RoleHero.currLevel:.0f}", int(0.5467*Y))
                pygame_print(f"Exp = {RoleHero.currExp:.2f} / {RoleHero.LevelExp:.2f}", int(0.6*Y))
                pygame.display.update()
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_RETURN:
                    print("exiting menu")
                    return


# prints a long pygame message
def long_pygame_print(message, count=0, line_break=24, color=black, background_color=white, offset_x=0, start_height=int(0.12*Y), thresh = 0.9):
    global X, Y, font, font_size, base_screen_height, base_font_height, base_font_size
    font_size = base_font_size
    font = pygame.font.Font('freesansbold.ttf', font_size)
    threshold = thresh * X
    scaled_font_height = (Y * base_font_height) / base_screen_height

    font_sz = font.size(message)
    while font_size > 1 and (font_sz[0] > threshold or font_sz[1] > scaled_font_height):
        font_size -= 1
        font = pygame.font.Font('freesansbold.ttf', font_size)
        font_sz = font.size(message)

    font = pygame.font.Font('freesansbold.ttf', font_size)

    temp = ""
    message = message.split()
    for token in message:
        if len(temp) + len(token) + 1 > line_break:
            pygame_print(temp, loc_y=start_height + count, color=color, background_color=background_color, offset_x=offset_x, thresh = thresh)
            count += int(0.0534 * Y)
            temp = token
        else:
            temp += " " + token

    pygame_print(temp, loc_y=start_height + count, color=color, background_color=background_color, offset_x=offset_x, thresh = thresh)
    return count


def AddButton(text="STOP", offset_x=0, loc_y=int(0.048*Y), background_color=red, font_size=int(0.03467*Y)):
    global font
    font = pygame.font.Font('freesansbold.ttf', font_size)
    stop_rect = pygame_print(text, loc_y=loc_y, background_color=background_color, offset_x=offset_x)
    font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))

    return stop_rect

def Mine(role, setting):
    '''
    Objective: Click on the object before
    the NPC snatches the item (before npcTime elapses)
    '''

    global time, font, X, Y, screen
    screen.fill(white)
    TheSetting = setting.name.upper()
    pygame_print("The objective of this game", loc_y = 0.12*Y)
    pygame_print("is to click on the item in time", loc_y = 0.20*Y)
    pygame_print("(To stop, click 'stop')!", loc_y = 0.28*Y)
    pygame.display.update()
    Opponent = NeutralNPC()
    wait_til_enter()
    screen.fill(white)
    pygame_print("Get ready, you are about to face:", loc_y = 0.12*Y)
    pygame_print(f"The {Opponent.role}", loc_y = int(0.20*Y))
    pygame.display.update()
    wait_til_enter()
    screen.fill(white)
    displayImageCustom(role.image_name, width = X//2, height = Y, loc_x = 0, loc_y = 0)
    #TODO: Get Images for Neutral NPCs and display the neural NPC below
    displayImageCustom(Opponent.image_name, width = X//2, height = Y, loc_x = X//2, loc_y = 0)
    
    pygame.display.update()
    wait_til_enter()
    screen.fill(white)

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

        font_sz = int(0.0267*Y)
        font = pygame.font.Font('freesansbold.ttf', font_sz)
        txt = f"Player Wins = {wins}\n{Opponent.role} Wins = {losses}\nDraws = {draws}"
        pygame_print(f"Player Wins = {wins}", loc_y=int(0.1334*Y))
        pygame_print(f"{Opponent.role} Wins = {losses}", loc_y=int(0.1867*Y))
        pygame_print(f"Draws = {draws}", loc_y=int(0.24*Y))

        stop_rect = AddButton(loc_y = int(0.048*Y), font_size = font_sz)

        pygame.draw.line(screen, black, (int(0.1*X), int(0.35*Y)), (int(0.9*X), int(0.35*Y)))  # top edge
        pygame.draw.line(screen, black, (int(0.1*X), int(0.9*Y)), (int(0.9*X), int(0.9*Y)))  # bottom edge
        pygame.draw.line(screen, black, (int(0.1*X), int(0.35*Y)), (int(0.1*X), int(0.9*Y)))  # left edge
        pygame.draw.line(screen, black, (int(0.9*X), int(0.35*Y)), (int(0.9*X), int(0.9*Y)))  # right edge

        # Determine coordinates where object will appear on the screen
        buffer_width_x, buffer_width_y = int(0.05*X), int(0.0534*Y)

        rand_X, rand_Y = randint(int(0.1*X) + buffer_width_x, int(0.9*X) - buffer_width_x), randint(int(0.35*Y) + buffer_width_y, int(0.9*Y) - buffer_width_y)

        square_rect = pygame.Rect(rand_X, rand_Y, buffer_width_x, buffer_width_y)

        item = np.random.choice(MinableItems, p=MineItemsProbs)
        image = pygame.image.load(MineImagesDict[item])
        image = pygame.transform.scale(image, (buffer_width_x, buffer_width_y))

        pygame.draw.rect(screen, white, square_rect)
        screen.blit(image, square_rect.topleft)

        pygame.display.update()
        #
        #        #pygame.time.delay(1000)  # waiting one second
        

        start = time()
        npcTime = 1 + (1 * random())
        botavg.append(npcTime)
        breakFlag = False
        playerTime = None
        mouse_pos = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    temp_X, temp_Y = X, Y
                    X, Y = screen.get_width(), screen.get_height()
                    X = 410 if X < 410 else X
                    print(f"X, Y = {X}, {Y}")
                    screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                    screen.fill(white)
                    font_sz = int(0.0267*Y)
                    font = pygame.font.Font('freesansbold.ttf', font_sz)
                    pygame_print(f"Player Wins = {wins}", loc_y=int(0.1334*Y))
                    pygame_print(f"{Opponent.role} Wins = {losses}", loc_y=int(0.1867*Y))
                    pygame_print(f"Draws = {draws}", loc_y=int(0.24*Y))
                    stop_rect = AddButton(loc_y = int(0.048*Y), font_size = font_sz)
                    pygame.draw.line(screen, black, (int(0.1*X), int(0.35*Y)), (int(0.9*X), int(0.35*Y)))  # top edge
                    pygame.draw.line(screen, black, (int(0.1*X), int(0.9*Y)), (int(0.9*X), int(0.9*Y)))  # bottom edge
                    pygame.draw.line(screen, black, (int(0.1*X), int(0.35*Y)), (int(0.1*X), int(0.9*Y)))  # left edge
                    pygame.draw.line(screen, black, (int(0.9*X), int(0.35*Y)), (int(0.9*X), int(0.9*Y)))  # right edge
                    # Determine coordinates where object will appear on the screen
                    buffer_width_x, buffer_width_y = int(0.05*X), int(0.0534*Y)
                    rand_X, rand_Y = (X/temp_X)*rand_X, (Y/temp_Y)*rand_Y
                    
                    square_rect = pygame.Rect(rand_X, rand_Y, buffer_width_x, buffer_width_y)
                    image = pygame.image.load(MineImagesDict[item])
                    image = pygame.transform.scale(image, (buffer_width_x, buffer_width_y))

                    pygame.draw.rect(screen, white, square_rect)
                    screen.blit(image, square_rect.topleft)

                    pygame.display.update()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
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

    #        #pygame.time.delay(1000)  # waiting one second

    playeravglen = (len(playeravg)) if len(playeravg) != 0 else 1
    playeravg = sum(playeravg)
    botavglen = (len(botavg)) if len(botavg) != 0 else 1
    botavg = sum(botavg)
    points = wins - losses

    netExp = points * Opponent.expYield if points >= 0 else 0

    increaseExp(role, netExp)
    screen.fill(white)
    font_sz = int(0.0267*X)
    font = pygame.font.Font('freesansbold.ttf', font_sz)
    
    if playeravg / playeravglen < botavg / botavglen:
        pygame_print("You get 5 extra resources", int(0.12*Y))
        pygame_print("because your avg was better", int(0.1734*Y))
        pygame_print(f"than the {Opponent.role}", int(0.2267*Y))

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

    pygame_print("The player average is {:.2f} seconds".format(playeravg / playeravglen), loc_y=int(0.28*Y))
    pygame_print("The {} average is {:.2f} seconds".format(Opponent.role, botavg / botavglen), loc_y=int(0.3333*Y))
    pygame_print("You got {} resources in total!".format(points), loc_y=int(0.3867*Y))
    pygame_print("You won {} games!".format(wins), loc_y=int(0.44*Y))
    pygame_print("You lost {} games!".format(losses), loc_y=int(0.4933*Y))
    pygame_print("{} is the number of games that drawed!".format(draws), loc_y=int(0.5467*Y))

    pygame.display.update()
    while True:
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)
                font_sz = int(0.0267*X)
                font = pygame.font.Font('freesansbold.ttf', font_sz)
                if playeravg / playeravglen < botavg / botavglen:
                    pygame_print("You get 5 extra resources", int(0.12*Y))
                    pygame_print("because your avg was better", int(0.1734*Y))
                    pygame_print(f"than the {Opponent.role}", int(0.2267*Y))
                pygame_print("The player average is {:.2f} seconds".format(playeravg / playeravglen), loc_y=int(0.28*Y))
                pygame_print("The {} average is {:.2f} seconds".format(Opponent.role, botavg / botavglen), loc_y=int(0.3333*Y))
                pygame_print("You got {} resources in total!".format(points), loc_y=int(0.3867*Y))
                pygame_print("You won {} games!".format(wins), loc_y=int(0.44*Y))
                pygame_print("You lost {} games!".format(losses), loc_y=int(0.4933*Y))
                pygame_print("{} is the number of games that drawed!".format(draws), loc_y=int(0.5467*Y))
                pygame.display.update()
                
            if event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_RETURN:
                    return points


def printItem(role, item_name):
    global font, white, black, orange
    screen.fill(white)  # clear the screen

    square_rect = pygame.Rect(int(0.05*X), int(0.1334*Y), int(0.4*X), int(0.31334*Y))  # left, top, width, height
    image = pygame.image.load(cppStringConvert(role.stringInv[item_name]["Picture"]))
    image = pygame.transform.scale(image, (int(0.4*X), int(0.31334*Y)))

    pygame.draw.rect(screen, white, square_rect)
    screen.blit(image, square_rect.topleft)

    pygame_print(f"Name: {item_name}", offset_x=-int(0.25*X), loc_y=int(0.5067*Y))
    pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25*X), loc_y=int(0.5867*Y))
    long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25*X),
                      line_break=23, start_height=int(0.7334*Y))

    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25*X), loc_y=int(0.2667*Y))
    pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25*X), loc_y=int(0.3467*Y))
    pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25*X), loc_y=int(0.4267*Y))
    pygame_print(f"Quest Level: {role.numInv[item_name]['QuestLevel']}", offset_x=int(0.25*X), loc_y=int(0.5067*Y))

    rect = AddButton(text="Use", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=orange)

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
                    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25*X), loc_y=int(0.2667*Y))
                    pygame.display.update()
            #TODO: Change color of "Use" button while hovering over
            elif rect.collidepoint(pygame.mouse.get_pos()):
                rect = AddButton(text="Use", offset_x=int(0.25 * X), loc_y=int(0.7334*Y), background_color=orange)
                pygame.display.update()
            elif not rect.collidepoint(pygame.mouse.get_pos()):
                rect = AddButton(text="Use", offset_x=int(0.25 * X), loc_y=int(0.7334*Y), background_color=green)
                pygame.display.update()

def sellItem(role, item_name):
    global font, white, black, orange, screen, X, Y
    screen.fill(white)  # clear the screen

    square_rect = pygame.Rect(int(0.05*X), int(0.1334*Y), int(0.4*X), int(0.31334*Y))  # left, top, width, height

    image = pygame.image.load(cppStringConvert(role.stringInv[item_name]["Picture"]))
    
    image = pygame.transform.scale(image, (int(0.4*X), int(0.3133*Y)))
    
    num_item = 0 #Count the amount of item_name that the user wants to buy
    max_amount = int(role.numInv[item_name]['Number'])

    pygame.draw.rect(screen, white, square_rect)
    screen.blit(image, square_rect.topleft)
    pygame_print(f"Name: {item_name}", offset_x=-int(0.25*X), loc_y=int(0.5067*Y), thresh=0.45)
    pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
    long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25*X), start_height=int(0.6667*Y), thresh=0.45)
    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
    pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
    pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
    pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
    font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
    pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
    font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
    pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)


    rect = AddButton(text="Sell", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=green)
#    on_sell_rect = False

    pygame.display.update()

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                square_rect = pygame.Rect(int(0.05*X), int(0.1334*Y), int(0.4*X), int(0.31334*Y))  # left, top, width, height
                image = pygame.image.load(cppStringConvert(role.stringInv[item_name]["Picture"]))
                image = pygame.transform.scale(image, (int(0.4*X), int(0.3133*Y)))
                pygame.draw.rect(screen, white, square_rect)
                screen.blit(image, square_rect.topleft)
                pygame_print(f"Name: {item_name}", offset_x=-int(0.25*X), loc_y=int(0.5067*Y), thresh=0.45)
                pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25*X), start_height=int(0.6667*Y), thresh=0.45)
                pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
                pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
                pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
                pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
                pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
                pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)
                rect = AddButton(text="Sell", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=green)
                pygame.display.update()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 0
                elif event.key == pygame.K_DOWN:
                    num_item = num_item - 1 if num_item != 0 else max_amount
                elif event.key == pygame.K_UP:
                    num_item = num_item + 1 if num_item != max_amount else 0
                    
                screen.fill(white)  # clear the screen
                pygame.draw.rect(screen, white, square_rect)
                screen.blit(image, square_rect.topleft)
                pygame_print(f"Name: {item_name}", offset_x=-int(0.25*X), loc_y=int(0.5067*Y), thresh=0.45)
                pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25*X), start_height=int(0.6667*Y), thresh=0.45)
                pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
                pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
                pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
                pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
                pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
                pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)
                rect = AddButton(text="Sell", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=green)
                pygame.display.update()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:  # checking if the mouse was clicked on the window
                mouse_pos = pygame.mouse.get_pos()
                if rect.collidepoint(mouse_pos):
                    print("Selling the item.")
                    role.numInv[item_name]['Number'] -= num_item
                    role.money += num_item * role.numInv[item_name]['SellValue']
                    max_amount = int(role.numInv[item_name]['Number'])
                    num_item = 0

                    screen.fill(white)  # clear the screen
                    pygame.draw.rect(screen, white, square_rect)
                    screen.blit(image, square_rect.topleft)
                    pygame_print(f"Name: {item_name}", offset_x=-int(0.25*X), loc_y=int(0.5067*Y), thresh=0.45)
                    pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                    long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25*X), start_height=int(0.6667*Y), thresh=0.45)
                    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
                    pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
                    pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
                    pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
                    font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
                    pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                    font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
                    pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)
                    rect = AddButton(text="Sell", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=green)
                    pygame.display.update()
                    
                    
            elif rect.collidepoint(pygame.mouse.get_pos()):# and not on_sell_rect:
                screen.fill(white)  # clear the screen
                pygame.draw.rect(screen, white, square_rect)
                screen.blit(image, square_rect.topleft)
                pygame_print(f"Name: {item_name}", offset_x=-int(0.25*X), loc_y=int(0.5067*Y), thresh=0.45)
                pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25*X), start_height=int(0.6667*Y), thresh=0.45)
                pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
                pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
                pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
                pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
                pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
                pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)
                rect = AddButton(text="Sell", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=orange)
#                on_sell_rect = True
                pygame.display.update()
            elif not rect.collidepoint(pygame.mouse.get_pos()):# and on_sell_rect:
                screen.fill(white)  # clear the screen
                pygame.draw.rect(screen, white, square_rect)
                screen.blit(image, square_rect.topleft)
                pygame_print(f"Name: {item_name}", offset_x=-int(0.25*X), loc_y=int(0.5067*Y), thresh=0.45)
                pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25*X), start_height=int(0.6667*Y), thresh=0.45)
                pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
                pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
                pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
                pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
                pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
                font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
                pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)
                rect = AddButton(text="Sell", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=green)
#                on_sell_rect = False
                pygame.display.update()

def buyItem(role, item_name):
    global font, white, black, orange, X, Y, screen
    screen.fill(white)  # clear the screen

    square_rect = pygame.Rect(int(0.05*X), int(0.1334*Y), int(0.4*X), int(0.31334*Y))  # left, top, width, height
    image = pygame.image.load(cppStringConvert(role.stringInv[item_name]["Picture"]))
    image = pygame.transform.scale(image, (int(0.4*X), int(0.3133*Y)))
    
    num_item = 0 #Count the amount of item_name that the user wants to buy
    max_amount = int(role.money // role.numInv[item_name]['BuyValue'])

    pygame.draw.rect(screen, white, square_rect)
    screen.blit(image, square_rect.topleft)
    pygame_print(f"Name: {item_name}", offset_x=-int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
    pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25 * X), loc_y=int(0.5867 * Y), thresh=0.45)
    long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25 * X), start_height=int(0.6667 * Y), thresh=0.45)
    pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
    pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
    if role.numInv[item_name].count('SellValue'):
        pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
    pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
    font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
    pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
    font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
    pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)

    pygame.display.update()
    rect = AddButton(text="Buy", offset_x=int(0.25*X), loc_y=int(0.7334*Y), background_color=green)
    
    while True:
        
        screen.fill(white)  # clear the screen
        
        pygame.draw.rect(screen, white, square_rect)
        screen.blit(image, square_rect.topleft)
        pygame_print(f"Name: {item_name}", offset_x=-int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
        pygame_print(f"Type: {cppStringConvert(role.stringInv[item_name]['Type'])}", offset_x=-int(0.25 * X), loc_y=int(0.5867 * Y), thresh=0.45)
        long_pygame_print(f"Description: {cppStringConvert(role.stringInv[item_name]['Description'])}", offset_x=-int(0.25 * X), start_height=int(0.6667 * Y), thresh=0.45)
        pygame_print(f"Amount: {role.numInv[item_name]['Number']}", offset_x=int(0.25 * X), loc_y=int(0.2667 * Y), thresh=0.45)
        pygame_print(f"Buy Value: {role.numInv[item_name]['BuyValue']}", offset_x=int(0.25 * X), loc_y=int(0.3467 * Y), thresh=0.45)
        if role.numInv[item_name].count('SellValue'):
            pygame_print(f"Sell Value: {role.numInv[item_name]['SellValue']}", offset_x=int(0.25 * X), loc_y=int(0.4267 * Y), thresh=0.45)
        pygame_print(f"Your Money:", offset_x=int(0.25 * X), loc_y=int(0.5067 * Y), thresh=0.45)
        font = pygame.font.Font('freesansbold.ttf', int(0.03333*Y))
        pygame_print(f"{role.money:.2f}", offset_x=int(0.25*X), loc_y=int(0.5867*Y), thresh=0.45)
        font = pygame.font.Font('freesansbold.ttf', int(0.04267*Y))
        pygame_print(f"How many?: {num_item}", offset_x=int(0.25*X), loc_y=int(0.6667*Y), thresh=0.45)

        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                square_rect = pygame.Rect(int(0.05*X), int(0.1334*Y), int(0.4*X), int(0.31334*Y))  # left, top, width, height
                image = pygame.image.load(cppStringConvert(role.stringInv[item_name]["Picture"]))
                image = pygame.transform.scale(image, (int(0.4*X), int(0.3133*Y)))
                pygame.draw.rect(screen, white, square_rect)
                screen.blit(image, square_rect.topleft)
            elif event.type == pygame.KEYDOWN:
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
                rect = AddButton(text="Buy", offset_x=int(0.25 * X), loc_y=int(0.84*Y), background_color=orange)
                pygame.display.update()
            elif not rect.collidepoint(pygame.mouse.get_pos()):
                rect = AddButton(text="Buy", offset_x=int(0.25 * X), loc_y=int(0.84*Y), background_color=green)
                pygame.display.update()


def getItemCounts(role):
    line_count = int(0.1067*Y)
    temp = line_count
    temp_2 = line_count//2
    currentInventory = {}
    for item in role.numInv:
        for attr in item.second:
            if cppStringConvert(attr.first) == "Number" and attr.second > 0:
                item_name = cppStringConvert(item.first)
                pygame_print(f"{item_name}: {attr.second}", loc_y=line_count, color=orange if line_count == temp else black)
                currentInventory[item_name] = attr.second
                line_count += temp_2

    return currentInventory, (line_count - temp) // temp_2

def print_no_items():
    global screen, X, Y
    pygame_print("You don't have any items.", loc_y=Y // 2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)
                pygame_print("You don't have any items.", loc_y=Y // 2)
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def printInventory(role):
    global font, white, black, orange, screen, X, Y
    optionNumber = 0

    while True:
        temp = int(0.1067*Y)
        temp_2 = temp//2
        screen.fill(white)
        line_count = temp
        currentInventory, num_items = getItemCounts(role)
        if num_items == 0:
            print_no_items()
            return
        currentInventoryList = list(currentInventory.keys())
        for idx, item in enumerate(currentInventory):
            pygame_print(f"{item}: {currentInventory[item]}", loc_y=line_count,
                         color=orange if idx == optionNumber else black)
            line_count += temp_2

        stop_rect = AddButton(text="EXIT", offset_x=0, loc_y = int(0.048*Y))
        pygame.display.update()

        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:  # checking if any key was selected
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

#https://stackoverflow.com/a/64745177/18255427
#Returns true if the range x_start, y_start overlaps with the range x_end, y_end
def overlaps(x_start, x_end, y_start, y_end):
    return max(x_start, y_start) < min(x_end, y_end)

'''
Rolling a dice:
 - 6 possibilities: {1, 2, 3, 4, 5, 6}, each with probability 1/6
 - E(x = outcome): sum_{i=1}^{n=6} possibility_i * prob_i = 1*1/6 + 2*1/6 + 3*1/6 + 4*1/6 + 5*1/6 + 6*1/6 = 1/6+2/6+3/6+4/6+5/6+6/6 = 27/6 = 3.5
 
'''

def QuestGames(Setting, role):
    global font, white, black, orange, X, Y, red
    role.health = role.base_health  # TODO: delete!
    role.attackpower = 1000  # TODO: delete!
    money = 0
    role_image_name = role.name.lower().replace(" jackson", "") + "-start.png"
    role_image_name_flipped = role_image_name.replace(".png", "flip.png")
    enemy_image_names = {"NINJA": "ninja.png", "OGRE": "ogre.png", "DEMON": "demon.png"}
    enemy_image_names_flipped = {"NINJA": "ninjaflip.png", "OGRE": "ogreflip.png", "DEMON": "demonflip.png"}

    buffer_width, buffer_height = int(.05*X), int(0.05334*Y)
    beam_height = buffer_height / 4
    beam_width = buffer_width / 2

    '''
    🤺            ⬬            ⬬                 👹
    (100,600)   (300, 600)     (400, 600)         (660, 600)
    
                                              ⬬
                                              (580, 670)
    
    Focus on beam closest to agent (in this case, the one at (400, 600))
    
    
    '''

    start_x, start_y, curr_y, enemy_x, enemy_y, curr_enemy_y = int(0.125*X), int(0.8*Y), int(0.8*Y), int(0.875*X) - buffer_width, int(0.8*Y), int(0.8*Y)
    ground_y = int(0.8*Y)

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
    dd = 5

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
    TotalEnemyBaseHealth = getEnemyBaseHealth()
    
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
        pygame_print(f"Quest #{role.questLevel + 1}", loc_y=0.08*Y)
       
        # Role Health Bar Health Bar
        #min(Y) = 150, min(X) = 165, max(Y) = 252, max(X) = 335
        pygame.draw.rect(screen, white, (0.1875*X, 0.18266*Y, 0.25*X, 0.16*Y))
        font = pygame.font.Font('freesansbold.ttf', int(0.029333333333333333*Y))
        pygame_print(cppStringConvert(role.name), loc_y = 0.2*Y, offset_x=-0.1875*X)
        font = pygame.font.Font('freesansbold.ttf', int(0.02667*Y))
        pygame_print("Lv. = "+ str(role.currLevel), loc_y=0.233*Y, offset_x=-0.14375*X)
        font = pygame.font.Font('freesansbold.ttf', int(0.02933*Y))
        pygame.draw.rect(screen, black, (0.20625*X, 0.26*Y, 0.1875*X, 0.02667*Y)) #165 -> 165/800*X, 195 -> 195/750*Y
        pygame.draw.rect(screen, green, (0.20625*X, 0.26*Y, 0.1875*X*role.health/role.base_health, 0.02667*Y)) #Health bar
        font = pygame.font.Font('freesansbold.ttf', int(0.02667*Y))
        pygame_print(f"{role.health:.0f} / {role.base_health:.0f}", loc_y=0.30667*Y, offset_x=-0.15625*X)
        font = pygame.font.Font('freesansbold.ttf', int(0.02933*Y))
        pygame.draw.rect(screen, black, (0.20625*X, 0.32266*Y, 0.2125*X, 0.01333*Y))
        pygame.draw.rect(screen, cyan, (0.20625*X, 0.32266*Y, 0.2125*X*role.currExp/role.LevelExp, 0.01333*Y)) #Exp bar
        
        role_image = pygame.image.load(
            f"Assets/{role_image_name}" if not role.flipped else f"Assets/{role_image_name_flipped}")
        role_image = pygame.transform.scale(role_image, (buffer_width, buffer_width))
        screen.blit(role_image, role_rect.topleft)
        
        # Enemy Health Bar
        #min(Y) = 170, min(X) = 485, max(Y) = 230, max(X) = 635
        pygame.draw.rect(screen, white, (0.58125*X, 0.18667*Y, 0.2375*X, 0.16*Y))

        pygame_print(cppStringConvert(enemy.name), loc_y = 0.22667*Y, offset_x=0.1875*X)
        pygame.draw.rect(screen, black, (0.60625*X, 0.26*Y, 0.1875*X, 0.02667*Y))
        pygame.draw.rect(screen, red, (0.60625*X, 0.26*Y, 0.1875*X*enemy.health/enemy.base_health, 0.02667*Y)) #Health bar
        font = pygame.font.Font('freesansbold.ttf', int(0.02667*Y))
        pygame_print(f"{enemy.health:.0f} / {enemy.base_health:.0f}", loc_y=0.306667*Y, offset_x=0.23375*X)
        font = pygame.font.Font('freesansbold.ttf', int(0.02933*Y))
        
        enemy_image = pygame.image.load(
            f"Assets/{enemy_image_names[enemy.name]}" if not enemy.flipped else f"Assets/{enemy_image_names_flipped[enemy.name]}")
        enemy_image = pygame.transform.scale(enemy_image, (buffer_width, buffer_width))
        screen.blit(enemy_image, enemy_rect.topleft)
        font = pygame.font.Font('freesansbold.ttf', int(0.04266*Y))

    role_rect = pygame.Rect(start_x, start_y, buffer_width, buffer_width)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, buffer_width, buffer_width)
    renderRole(start_x, start_y)

    shotsFired = []
    shotsEnemyFired = []
    K = 10  # Constant factor for gravity

    global badNPCs  # we're saying that we will be using the global variable badNPCs
    NumberDefeated = 0

    start_msg_time = time()
    start_msg_interval = 2  # At the beginning of each round, a message saying 'spawning new enemy' will appear for 2 seconds

    def generateMove(temp_state):
        '''
        Generate a move that the agent should make based on the UCT   a:
            UCT = Q(s,a) + c*sqrt( ln(N(s)) / N(s,a) )
        
        Returns: index corresponding to element in enemy_options list that enemy should make
        '''

        UCT = 0
        UCT_best = -np.inf
        best_act = "none"
        best_acts = []

        for enemy_option in enemy_options:
            # If the condition below is true then we can use the UCT formula
            if Nsa.get(temp_state) and int(Nsa[temp_state].get(enemy_option) or 0) > 0 and Qsa.get(temp_state) and Qsa.get(temp_state).get(enemy_option):
                UCT = Qsa[temp_state][enemy_option] + c * sqrt(ln(Ns[temp_state] / Nsa[temp_state][enemy_option]))
            else:
                best_acts.append(enemy_option)
                UCT = -np.inf  # encourage this action since it has no visit counts
            if UCT > UCT_best:
                best_act = enemy_option
                UCT_best = UCT
        
        if best_act != "none":
            best_acts.append(best_act)
        if len(best_acts) > 0:
            best_act = np.random.choice(best_acts)

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
    score = 0
    avg_score = 0
    update_iter = 150
    while True:  # pygame loop
        if n_iter != 0 and n_iter % update_iter == 0:
            if check_point_score == max_score: #if no new max
                score_ratio = avg_score/(update_iter*(max_score or max_score + np.finfo(float).eps))
                print(f"avg_score/max_score = {score_ratio}")
                if random() >= score_ratio:
                    c = c + sqrt(2)
                    print(f"Increasing exploration, no luck, c = {c}")
                else:
                    c = sqrt(2)
                    print(f"Lucky, resetting exploration, c = {c}")
            else:
                c = sqrt(2) #Keep exploration the same
                print(f"New max, resetting exploration, c = {c}")

                check_point_score = max_score
            avg_score = 0

        n_iter += 1
        last_role_health = role.health
        last_agent_health = getEnemyHealth()  # enemy.health
        #800*750*800*750*1000*2 = 7.2*10^14 possible states?
        
#        temp_state = f"agent_x = {enemy_x:0.0f}, agent_y = {curr_enemy_y:0.0f}, role_x = {start_x:0.0f}, role_y = {curr_y:0.0f}, agent_health = {last_agent_health / TotalEnemyBaseHealth:0.0f}, agent_flipped = {enemy.flipped}, shotsFired = {shotsFired}" #last_agent_health / TotalEnemyBaseHealth
    
        DangerShotVal = abs(enemy_x - start_x) if curr_y - beam_height <= enemy_y <= curr_y + beam_height else max(X - enemy_x, enemy_x)
        '''
        E.g. enemy_x = 450 -> DangerShotVal = max(800-450, 450) = max(350, 450) = 450
             enemy_x = 350 -> DangerShotVal = max(800-350, 350) = max(450, 350) = 450

        (0,0)     (350,0)       (800,0)  --> DangerShotVal = 450
        (0,0)         (450,0)   (800,0)  --> DangerShotVal = 450
        '''
        if len(shotsFired):
            '''
            We want to check if the range (shot.beam_y - beam_height, shot.beam_y + beam_height) intersects with the range (enemy_y, enemy_y + buffer_width)
            [620, 640], [600, 640]
            
            [420, 440], [500, 540]
            '''
            
            DangerShots = [shot for shot in shotsFired if overlaps(shot.beam_y - beam_height, shot.beam_y + beam_height, enemy_y, enemy_y + buffer_width) and not shot.hit_target]
            if len(DangerShots):
                DangerShot = min(DangerShots, key = lambda shot: abs(enemy_x - shot.beam_x)) #The closest danger shot to the enemy (agent)
                DangerShotVal = min(abs(enemy_x - DangerShot.beam_x), DangerShotVal)
                
        temp_state = int(DangerShotVal)
            
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
                elif event.key in role.InputMapDict and role.numInv[role.InputMapDict[event.key]]["Number"] > 0:
#                    print(f"{event.key} is in {role.InputMapDict}")
                    role.useInv[role.InputMapDict[event.key]]["Use"]()
                    if role.isSpecialShot:
                        if role.can_attack():
                            beam_x = start_x + (buffer_width if not role.flipped else 0)
                            beam_y = curr_y + buffer_width / 2
                            # Puts the coordinate of the shots fired on the screen
                            shotsFired.append(Shot(beam_x, beam_y, False,
                                                   role.flipped, True, role.specialShotImage))  # x-position of beam, y-position of beam, has it hit the target?, flipped?
                            # Update the wait-time here.
                            role.update_wait_time()
                        else:
                            role.numInv[role.InputMapDict[event.key]]["Number"] += 1

        if enemy_options[enemyMove] == "jump" and enemy_y + int(0.2666*Y) >= ground_y:  # Holding down jump makes it bigger
            curr_enemy_y -= 0.006666666666666667*Y
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
            s = ((K * 0.5 * 9.81 * fall_time ** 2)/750)*Y  # The absolute value the hero has fallen since role_jump_t

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
            s = ((K * 0.5 * 9.81 * fall_time ** 2)/750)*Y
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
            if curr_y + int(0.2666*Y) >= ground_y:  # Check if they can keep going higher, curr_y must >= 400 atm (less than 200 elevation)
                curr_y -= int(0.00666*Y)
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
            shot.beam_x = shot.beam_x + role.shot_speed if not shot.is_flipped else shot.beam_x - role.shot_speed
            beam_rect = pygame.Rect(shot.beam_x, shot.beam_y, beam_width,
                                    beam_height)  # beam object
            if beam_rect.colliderect(
                    enemy_rect) and not shot.hit_target:  # Enemy was hit and this is not a repeat of the same shot
                role.attack(enemy, multiplier = 1 if not shot.is_special_shot else role.specialShotMultipliers[role.specialShotImage])
                pygame.draw.rect(screen, red, enemy_rect, 2)
                if enemy.health == 0:
                    money += enemy.expYield*10
                    increaseExp(role, enemy.expYield)
                    NumberDefeated += 1
                    renderRole(start_x, curr_y)
                    if NumberDefeated < 10:
                        enemy = enemies[NumberDefeated]  # spawnBadNPC()
                        pygame_print(f"Spawning enemy #{NumberDefeated + 1}/10: {enemy.name}", loc_y=int(0.4*Y))
                        start_msg_time = time()
                    else:
                        role.questLevel += 1
                        role.money += money
                        pygame_print(f"You Won!!", loc_y=int(0.4*Y))

                shot.hit_target = True
            if not shot.is_special_shot:
                pygame.draw.ellipse(screen, orange, beam_rect)  # Drawing the beam
            else:
#                print(shot.special_image, cppStringConvert(shot.special_image))
                image = pygame.image.load(cppStringConvert(shot.special_image))
                image = pygame.transform.scale(image, (beam_width, beam_height))
                screen.blit(image, beam_rect.topleft)

        for shot in shotsEnemyFired:
            shot.beam_x = shot.beam_x - enemy.shot_speed if not shot.is_flipped else shot.beam_x + enemy.shot_speed
            beam_rect = pygame.Rect(shot.beam_x, shot.beam_y, beam_width, beam_height)  # beam object
            if beam_rect.colliderect(
                    role_rect) and not shot.hit_target:  # Role was hit and this is not a repeat of the same shot
                enemy.attack(role)
                pygame.draw.rect(screen, red, role_rect, 2)

                shot.hit_target = True
            pygame.draw.ellipse(screen, red, beam_rect)  # Drawing the beam

        #Deleting shots that have trailed off the page
        shotsFired = [shot for shot in shotsFired if shot.beam_x >= 0 and shot.beam_x <= X]
        shotsEnemyFired = [shot for shot in shotsEnemyFired if shot.beam_x >= 0 and shot.beam_x <= X]

        if role.health <= 0:
            pygame_print("You died!", loc_y=int(0.4*Y))
        elif time() - start_msg_time < start_msg_interval and NumberDefeated < 10:
            pygame_print(f"Spawning enemy #{NumberDefeated + 1}/10: {enemy.name}", loc_y=int(0.4*Y))

        pygame.display.update()

        if NumberDefeated == 10 or role.health <= 0:
            # Do stuff
            #pygame.time.delay(1000)
            wait_til_enter()
#            pygame.event.clear(eventtype=pygame.KEYDOWN)
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
        
        '''
        getEnemyBaseHealth()    getEnemyHealth()    dt
        --------------------    ----------------    --
        100                     40                  (100-40)/100 = 60/100 = 0.6
        100                     30                  (100-30)/100 = 70/100 = 0.7
        100                     100                 (100-100)/100 = 0/100 = 0
        
        
        '''
        
        score = 0.05 + (dd * (damage_dealt / role.base_health) - dt * (damage_taken / getEnemyBaseHealth()) * 1.3)
        avg_score += score
#        print(f"score = {score}, damage_dealt / role.base_health = {damage_dealt / role.base_health}, damage_dealt = {damage_dealt}")

        if score > max_score:
            max_score = score
            print(f"New max score, {max_score}")

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
    global X, Y, screen
    print(Role.numInv)
    if not HasSellableItems(Role.numInv):
        pygame_print("You don't have any sellable items!", 0.4*Y, color=black, background_color=white)
        pygame.display.update()
        #pygame.time.delay(1000)
        wait_til_enter()
#        pygame.event.clear(eventtype=pygame.KEYDOWN)
        return
    
    sellableItems = Role.printSellItemsVec(False, False)
    print(Role.numInv)
    
    optionNumber = 0
    maxItems = 3
    startSellIdx = 0
    endSellIdx = min(sellableItems.size(), maxItems)
    while True: #TODO: Inefficient,
        screen.fill(white)  # clear the screen
        pygame_print(f"What would you like to sell today?", (0.08*Y), color=black, background_color=white)
        pygame_print("=================================", (0.134*Y), color=black, background_color=white)
        text_y = (0.1867*Y)
        for i in range(startSellIdx, endSellIdx):
            pygame_print(sellableItems[i].title(), text_y, color=(orange if optionNumber == i else black), background_color=white)
            text_y += 0.05334*Y

        pygame_print(f"Your Money = {Role.money:0.2f}", text_y + 0.02667*Y, color=black, background_color=white)

        stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)

        pygame.display.update()
        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:  # checking if any key was selected
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
            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return


def BuyOption(Role):
    global screen, X, Y
    if Role.money == 0:
        pygame_print("You don't have any money!", (0.4*Y), color=black, background_color=white)
        pygame.display.update()
        #pygame.time.delay(1000)
        wait_til_enter()
#        pygame.event.clear(eventtype=pygame.KEYDOWN)
        return

    buyableItems = Role.printBuyItemsVec(False)
    print(Role.numInv)
    if buyableItems.size() == 0:
        pygame_print("You don't have enough money and/or", (0.4*Y), color=black, background_color=white)
        pygame_print("you haven't completed enough quests!", (0.4534*Y), color=black, background_color=white)
        pygame.display.update()
        #pygame.time.delay(1000)
        wait_til_enter()
#        pygame.event.clear(eventtype=pygame.KEYDOWN)
        return

    optionNumber = 0
    maxItems = 3
    startBuyIdx = 0
    endBuyIdx = min(buyableItems.size(), maxItems)
    
    while True:
        screen.fill(white)  # clear the screen
        pygame_print(f"What would you like to buy today?", (0.08*Y), color=black, background_color=white)
        pygame_print("=================================", (0.134*Y), color=black, background_color=white)
        text_y = (0.1867*Y)
        for i in range(startBuyIdx, endBuyIdx):
            pygame_print(buyableItems[i].title(), text_y, color=(orange if optionNumber == i else black), background_color=white)
            text_y += 0.05334*Y

        pygame_print(f"Your Money = {Role.money:0.2f}", text_y + 0.02667*Y, color=black, background_color=white)

        stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)

        pygame.display.update()
        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:  # checking if any key was selected
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
    global screen, X, Y
    optionNumber = 0
    Role.money = 1e6 #TODO: delete
    while True:
        screen.fill(white)  # clear the screen
        pygame_print("What would you like to do today?", (0.12*Y), color=black, background_color=white)
        pygame_print("================================", (0.1734*Y), color=black, background_color=white)
        pygame_print("Buy", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
        pygame_print("Sell", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)

        stop_button = AddButton(text="EXIT", offset_x=0, loc_y=(0.4134*Y), background_color=red)

        pygame.display.update()
        for event in pygame.event.get():  # update the option number if necessary for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
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
#                    pygame.event.clear(eventtype=pygame.KEYDOWN)

            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return

def DeleteInputMapKey(role):
    global X, Y, screen
    
    screen.fill(white)  # clear the screen
    if not role.InputMapDict: #If the input map dictionary is empty
        
        pygame_print("No keys have been mapped!", loc_y=Y // 2)
        pygame.display.update()
        wait_til_enter()
        return
    
    optionNumber = 0
    maxItems = 3
    startIdx = 0
    endIdx = min(len(role.InputMapDict), maxItems)
    
#    for key in role.InputMapDict:
#        pygame_print(key + " -> " + role.InputMapDict[key], ...)

    pygame_print(f"Select Key-Value Pair to Delete", (0.08*Y), color=black, background_color=white)
    pygame_print("===============================", (0.1334*Y), color=black, background_color=white)
    text_y = (0.1867*Y)
    for i in range(startIdx, endIdx):
        pygame_print(f"{pygame.key.name(role.InputMapDictKeys[i])}: {role.InputMapDict[role.InputMapDictKeys[i]]}", text_y, color=(red if optionNumber == i else black), background_color=white)
        text_y += 0.0533*Y
        
    stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)  # clear the screen
                pygame_print(f"Select Key-Value Pair to Delete", (0.08*Y), color=black, background_color=white)
                pygame_print("===============================", (0.1334*Y), color=black, background_color=white)
                text_y = (0.1867*Y)
                for i in range(startIdx, endIdx):
                    pygame_print(f"{pygame.key.name(role.InputMapDictKeys[i])}: {role.InputMapDict[role.InputMapDictKeys[i]]}", text_y, color=(red if optionNumber == i else black), background_color=white)
                    text_y += 0.0533*Y

                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
                pygame.display.update()
                
            elif event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != len(role.InputMapDict) - 1 else 0
                    if optionNumber == 0:
                        startIdx = 0
                    elif startIdx + 1 + maxItems <= len(role.InputMapDict) and optionNumber > startIdx - 1 + maxItems:
                        startIdx += 1
                    
                    endIdx = startIdx + min(len(role.InputMapDict), maxItems)
                                       
                    '''
                e.g. maxItems = 3,
                start: startIdx = 0, endIdx = 3
                    
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
                    optionNumber = optionNumber - 1 if optionNumber != 0 else len(role.InputMapDict) - 1
                    if optionNumber < startIdx:
                        startIdx = startIdx - 1 if startIdx - 1 >= 0 else 0
                    elif optionNumber > startIdx + maxItems - 1:
                        startIdx = optionNumber - maxItems + 1
                    endIdx = startIdx + min(len(role.InputMapDict), maxItems)
                
                elif event.key == pygame.K_RETURN:
                    del role.InputMapDict[role.InputMapDictKeys[optionNumber]]
                    del role.InputMapDictKeys[optionNumber]
                    
                    if len(role.InputMapDict) == 0:
                        return

                    optionNumber = 0
                    startIdx = 0
                    endIdx = min(len(role.InputMapDict), maxItems)
#                    screen.fill(white)
                
                screen.fill(white)  # clear the screen
                pygame_print(f"Select Key-Value Pair to Delete", (0.08*Y), color=black, background_color=white)
                pygame_print("===============================", (0.1334*Y), color=black, background_color=white)
                text_y = (0.1867*Y)
                for i in range(startIdx, endIdx):
                    pygame_print(f"{pygame.key.name(role.InputMapDictKeys[i])}: {role.InputMapDict[role.InputMapDictKeys[i]]}", text_y, color=(red if optionNumber == i else black), background_color=white)
                    text_y += 0.0533*Y
                    
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
                pygame.display.update()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return

def ViewInputMapKey(role):
    global X, Y, screen
    screen.fill(white)  # clear the screen
    if not role.InputMapDict:
        pygame_print("No keys have been mapped!")
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

    optionNumber = 0
    maxItems = 3
    startIdx = 0
    endIdx = min(len(role.InputMapDict), maxItems)

    #    for key in role.InputMapDict:
    #        pygame_print(key + " -> " + role.InputMapDict[key], ...)
    
    screen.fill(white)  # clear the screen
    pygame_print(f"View your mapped keys", (0.08*Y), color=black, background_color=white)
    pygame_print("===============================", (0.1334*Y), color=black, background_color=white)
    text_y = (0.1867*Y)
    for i in range(startIdx, endIdx):
        pygame_print(f"{pygame.key.name(role.InputMapDictKeys[i])}: {role.InputMapDict[role.InputMapDictKeys[i]]}", text_y, color=(orange if optionNumber == i else black), background_color=white)
        text_y += 0.05334*Y

    stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)

    pygame.display.update()

    while True:
        
        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)  # clear the screen
                pygame_print(f"View your mapped keys", (0.08*Y), color=black, background_color=white)
                pygame_print("===============================", (0.1334*Y), color=black, background_color=white)
                text_y = (0.1867*Y)
                for i in range(startIdx, endIdx):
                    pygame_print(f"{pygame.key.name(role.InputMapDictKeys[i])}: {role.InputMapDict[role.InputMapDictKeys[i]]}", text_y, color=(orange if optionNumber == i else black), background_color=white)
                    text_y += 0.05334*Y
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
                pygame.display.update()
                
            elif event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != len(role.InputMapDict) - 1 else 0
                    if optionNumber == 0:
                        startIdx = 0
                    elif startIdx + 1 + maxItems <= len(role.InputMapDict) and optionNumber > startIdx - 1 + maxItems:
                        startIdx += 1

                    endIdx = startIdx + min(len(role.InputMapDict), maxItems)

                elif event.key == pygame.K_UP:
                    optionNumber = optionNumber - 1 if optionNumber != 0 else len(role.InputMapDict) - 1
                    if optionNumber < startIdx:
                        startIdx = startIdx - 1 if startIdx - 1 >= 0 else 0
                    elif optionNumber > startIdx + maxItems - 1:
                        startIdx = optionNumber - maxItems + 1
                    endIdx = startIdx + min(len(role.InputMapDict), maxItems)
                    
                screen.fill(white)  # clear the screen
                pygame_print(f"View your mapped keys", (0.08*Y), color=black, background_color=white)
                pygame_print("===============================", (0.1334*Y), color=black, background_color=white)
                text_y = (0.1867*Y)
                for i in range(startIdx, endIdx):
                    pygame_print(f"{pygame.key.name(role.InputMapDictKeys[i])}: {role.InputMapDict[role.InputMapDictKeys[i]]}", text_y, color=(orange if optionNumber == i else black), background_color=white)
                    text_y += 0.05334*Y
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                    pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return

def printKeyError(key):
    screen.fill(white)
    pygame_print(f"ERROR, \"{pygame.key.name(key).upper()}\" CANNOT BE MAPPED!", color=red, background_color=white)
    pygame.display.update()
    wait_til_enter()
    
def AddInputMapKey(role):
    global X, Y, screen
    key = None
    breakFlag = False
    invalidKeys = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_RETURN, pygame.K_SPACE)
    screen.fill(white)  # clear the screen
    pygame_print("Select the key you would like to remap", (0.12*Y), color=black, background_color=white)
    pygame_print("================================", (0.1734*Y), color=black, background_color=white)
    stop_button = AddButton(text="EXIT", offset_x=0, loc_y=(0.4133*Y), background_color=red)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)
                pygame_print("Select the key you would like to remap", (0.12*Y), color=black, background_color=white)
                pygame_print("================================", (0.1734*Y), color=black, background_color=white)
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=(0.4133*Y), background_color=red)
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key in invalidKeys:
                    printKeyError(event.key)
                    screen.fill(white)
                    pygame_print("Select the key you would like to remap", (0.12*Y), color=black, background_color=white)
                    pygame_print("================================", (0.1734*Y), color=black, background_color=white)
                    stop_button = AddButton(text="EXIT", offset_x=0, loc_y=(0.4133*Y), background_color=red)
                    pygame.display.update()
                else:
                    key = event.key
                    breakFlag = True
                    break
            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return
        if breakFlag:
            break
                
    questItems = role.QuestItemsVec()
    
    optionNumber = 0
    maxItems = 3
    startIdx = 0
    endIdx = min(questItems.size(), maxItems)
    
    screen.fill(white)  # clear the screen
    pygame_print("Which item would you like to map", (0.08*Y), color=black, background_color=white)
    pygame_print(f"the key \"{pygame.key.name(key)}\" to?", (0.1334*Y), color=black, background_color=white)
    pygame_print("=================================", (0.1867*Y), color=black, background_color=white)
    text_y = (0.24*Y)
    for i in range(startIdx, endIdx):
        pygame_print(questItems[i].title(), text_y, color=(orange if optionNumber == i else black), background_color=white)
        text_y += 0.05334*Y
    stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
    pygame.display.update()
        
    while True:

        for event in pygame.event.get():  # update the option number if necessaryfor event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)  # clear the screen
                pygame_print("Which item would you like to map", (0.08*Y), color=black, background_color=white)
                pygame_print(f"the key \"{pygame.key.name(key)}\" to?", (0.1334*Y), color=black, background_color=white)
                pygame_print("=================================", (0.1867*Y), color=black, background_color=white)
                text_y = (0.24*Y)
                for i in range(startIdx, endIdx):
                    pygame_print(questItems[i].title(), text_y, color=(orange if optionNumber == i else black), background_color=white)
                    text_y += 0.05334*Y
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != questItems.size() - 1 else 0
                    if optionNumber == 0:
                        startIdx = 0
                    elif startIdx + 1 + maxItems <= questItems.size() and optionNumber > startIdx - 1 + maxItems:
                        startIdx += 1
                    
                    endIdx = startIdx + min(questItems.size(), maxItems)
                                       
                    '''
                e.g. maxItems = 3,
                start: startIdx = 0, endIdx = 3
                    
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
                    optionNumber = optionNumber - 1 if optionNumber != 0 else questItems.size() - 1
                    if optionNumber < startIdx:
                        startIdx = startIdx - 1 if startIdx - 1 >= 0 else 0
                    elif optionNumber > startIdx + maxItems - 1:
                        startIdx = optionNumber - maxItems + 1
                    endIdx = startIdx + min(questItems.size(), maxItems)
                    
                elif event.key == pygame.K_RETURN:
                    role.InputMapDict[key] = cppStringConvert(questItems[optionNumber])
#                    print(f"Key Value Pair: key = {chr(key)}, value = {role.InputMapDict[key]}"
                    if key not in role.InputMapDictKeys:
                        role.InputMapDictKeys.append(key)
                    return
                
                screen.fill(white)  # clear the screen
                pygame_print("Which item would you like to map", (0.08*Y), color=black, background_color=white)
                pygame_print(f"the key \"{pygame.key.name(key)}\" to?", (0.1334*Y), color=black, background_color=white)
                pygame_print("=================================", (0.1867*Y), color=black, background_color=white)
                text_y = (0.24*Y)
                for i in range(startIdx, endIdx):
                    pygame_print(questItems[i].title(), text_y, color=(orange if optionNumber == i else black), background_color=white)
                    text_y += 0.05334*Y
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=text_y + 0.10667*Y, background_color=red)
                pygame.display.update()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return

def InputMap(role):
    global X, Y, screen

    optionNumber = 0
    
    screen.fill(white)
    pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
    pygame_print("================", (0.1734*Y), color=black, background_color=white)
    pygame_print("Add Key to Input Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
    pygame_print("Delete Key from Input Map", (0.28*Y), color=(red if optionNumber == 1 else black), background_color=white)
    pygame_print("View Input Map", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
    stop_button = AddButton(text="EXIT", offset_x=0, loc_y=(0.3867*Y), background_color=red)

    pygame.display.update()

    while True:
        
        for event in pygame.event.get():  # update the option number if necessary
            if event.type == pygame.VIDEORESIZE:
                X, Y = screen.get_width(), screen.get_height()
                X = 410 if X < 410 else X
                print(f"X, Y = {X}, {Y}")
                screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                screen.fill(white)
                pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                pygame_print("================", (0.1734*Y), color=black, background_color=white)
                pygame_print("Add Key to Input Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                pygame_print("Delete Key from Input Map", (0.28*Y), color=(red if optionNumber == 1 else black), background_color=white)
                pygame_print("View Input Map", (0.3334*Y), color=(orange if optionNumber == 2 else black),
                background_color=white)
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=(0.3867*Y), background_color=red)

                pygame.display.update()
            elif event.type == pygame.KEYDOWN:  # checking if any key was selected
                if event.key == pygame.K_DOWN:
                    optionNumber = optionNumber + 1 if optionNumber != 2 else 0
                elif event.key == pygame.K_UP:
                    optionNumber = optionNumber - 1 if optionNumber != 0 else 2
                elif event.key == pygame.K_RETURN:
                    if optionNumber == 0:  # Add
                        AddInputMapKey(role)
                    elif optionNumber == 1:  # Delete
                        DeleteInputMapKey(role)
                    elif optionNumber == 2: #view
                        ViewInputMapKey(role)
                screen.fill(white)
                pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                pygame_print("================", (0.1734*Y), color=black, background_color=white)
                pygame_print("Add Key to Input Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                pygame_print("Delete Key from Input Map", (0.28*Y), color=(red if optionNumber == 1 else black), background_color=white)
                pygame_print("View Input Map", (0.3334*Y), color=(orange if optionNumber == 2 else black),
                background_color=white)
                stop_button = AddButton(text="EXIT", offset_x=0, loc_y=(0.3867*Y), background_color=red)

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(
                pygame.mouse.get_pos()):  # If the mouse was clicked on the stop button
                return

def Menu(role, setting):
    # Only going to execute once
    global Quests, orange, black, white, X, Y, screen
    if Quests == False:
        optionNumber = 0
        screen.fill(white)
        pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
        pygame_print("================", (0.1734*Y), color=black, background_color=white)
        pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
        pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
        pygame_print("Stats", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
        pygame.display.update()

        while True:
            for event in pygame.event.get():  # update the option number if necessary
                if event.type == pygame.VIDEORESIZE:
                    X, Y = screen.get_width(), screen.get_height()
                    X = 410 if X < 410 else X
                    print(f"X, Y = {X}, {Y}")
                    screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                    screen.fill(white)
                    pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                    pygame_print("================", (0.1734*Y), color=black, background_color=white)
                    pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                    pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
                    pygame_print("Stats", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
                    pygame.display.update()
                elif event.type == pygame.KEYDOWN:  # checking if any key was selected
                    if event.key == pygame.K_DOWN:
                        optionNumber = optionNumber + 1 if optionNumber != 2 else 0
                        
                        screen.fill(white)
                        pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                        pygame_print("================", (0.1734*Y), color=black, background_color=white)
                        pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                        pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
                        pygame_print("Stats", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
                        pygame.display.update()
                    elif event.key == pygame.K_UP:
                        optionNumber = optionNumber - 1 if optionNumber != 0 else 2
                        
                        screen.fill(white)
                        pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                        pygame_print("================", (0.1734*Y), color=black, background_color=white)
                        pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                        pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
                        pygame_print("Stats", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
                        pygame.display.update()
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
        screen.fill(white)
        pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
        pygame_print("================", (0.1734*Y), color=black, background_color=white)
        pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
        pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
        pygame_print("Mine", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
        pygame_print("Inv", (0.3867*Y), color=(orange if optionNumber == 3 else black), background_color=white)
        pygame_print("Shop", (0.44*Y), color=(orange if optionNumber == 4 else black), background_color=white)
        pygame_print("Quests", (0.4934*Y), color=(orange if optionNumber == 5 else black), background_color=white)
        pygame_print("Stats", (0.5467*Y), color=(orange if optionNumber == 6 else black), background_color=white)
        pygame_print("InputMap", (0.6*Y), color=(orange if optionNumber == 7 else black), background_color=white)
        pygame.display.update()
        while True:
            for event in pygame.event.get():  # update the option number if necessary
                if event.type == pygame.VIDEORESIZE:
                    X, Y = screen.get_width(), screen.get_height()
                    X = 410 if X < 410 else X
                    print(f"X, Y = {X}, {Y}")
                    screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                    screen.fill(white)
                    pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                    pygame_print("================", (0.1734*Y), color=black, background_color=white)
                    pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                    pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
                    pygame_print("Mine", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
                    pygame_print("Inv", (0.3867*Y), color=(orange if optionNumber == 3 else black), background_color=white)
                    pygame_print("Shop", (0.44*Y), color=(orange if optionNumber == 4 else black), background_color=white)
                    pygame_print("Quests", (0.4934*Y), color=(orange if optionNumber == 5 else black), background_color=white)
                    pygame_print("Stats", (0.5467*Y), color=(orange if optionNumber == 6 else black), background_color=white)
                    pygame_print("InputMap", (0.6*Y), color=(orange if optionNumber == 7 else black), background_color=white)
                    pygame.display.update()
                if event.type == pygame.KEYDOWN:  # checking if any key was selected
                    if event.key == pygame.K_DOWN:
                        optionNumber = optionNumber + 1 if optionNumber != 7 else 0
                        screen.fill(white)
                        pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                        pygame_print("================", (0.1734*Y), color=black, background_color=white)
                        pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                        pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
                        pygame_print("Mine", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
                        pygame_print("Inv", (0.3867*Y), color=(orange if optionNumber == 3 else black), background_color=white)
                        pygame_print("Shop", (0.44*Y), color=(orange if optionNumber == 4 else black), background_color=white)
                        pygame_print("Quests", (0.4934*Y), color=(orange if optionNumber == 5 else black), background_color=white)
                        pygame_print("Stats", (0.5467*Y), color=(orange if optionNumber == 6 else black), background_color=white)
                        pygame_print("InputMap", (0.6*Y), color=(orange if optionNumber == 7 else black), background_color=white)
                        pygame.display.update()
                    elif event.key == pygame.K_UP:
                        optionNumber = optionNumber - 1 if optionNumber != 0 else 7
                        screen.fill(white)
                        pygame_print("Choose an option", (0.12*Y), color=black, background_color=white)
                        pygame_print("================", (0.1734*Y), color=black, background_color=white)
                        pygame_print("Map", (0.2267*Y), color=(orange if optionNumber == 0 else black), background_color=white)
                        pygame_print("Search", (0.28*Y), color=(orange if optionNumber == 1 else black), background_color=white)
                        pygame_print("Mine", (0.3334*Y), color=(orange if optionNumber == 2 else black), background_color=white)
                        pygame_print("Inv", (0.3867*Y), color=(orange if optionNumber == 3 else black), background_color=white)
                        pygame_print("Shop", (0.44*Y), color=(orange if optionNumber == 4 else black), background_color=white)
                        pygame_print("Quests", (0.4934*Y), color=(orange if optionNumber == 5 else black), background_color=white)
                        pygame_print("Stats", (0.5467*Y), color=(orange if optionNumber == 6 else black), background_color=white)
                        pygame_print("InputMap", (0.6*Y), color=(orange if optionNumber == 7 else black), background_color=white)
                        pygame.display.update()
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
                        elif optionNumber == 7:
                            InputMap(role)
                        return

def game():
    global font, Quests, screen, old_screen, X, Y
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
        resized = False

        while True:
            pygame.display.update()
            
            for event in pygame.event.get():  # Can only call pygame.event.get() once per iteration
                if event.type == pygame.VIDEORESIZE:
                    X, Y = screen.get_width(), screen.get_height()
                    X = 410 if X < 410 else X
                    print(f"X, Y = {X}, {Y}")
                    screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
                    if displayedHeroes and not dispayedChest:
                        updateList(heroes, optionNumber, inc = 0.1*Y)
                    elif dispayedChest and not displayedPlaces:
                        displayImage("treasure_chest.png", p=1)
                        pygame_print(text = "Do you open the chest?", loc_y = Y // 1.5, color=black, background_color = white, offset_x=0)
                        openChestOption(optionNumber)  # Displaying 'Yes' and 'No'
                        
                if not started:
                    screen.fill(light_pink)
                    screen.blit(text, textRect)
                    pygame.display.update()
                    started = True
                    #old_screen = screen
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if not displayedHeroes:
                    #pygame.time.delay(1000)
                    print("displayedHeroes")
                    wait_til_enter()
                    updateList(heroes, optionNumber, inc = 0.1*Y)
                    displayedHeroes = True
                    #old_screen = screen
                elif displayedHeroes and not dispayedChest:
                    if event.type == pygame.KEYDOWN:  # checking if any key was selected
                        if event.key == pygame.K_DOWN:
                            optionNumber = optionNumber + 1 if optionNumber != 5 else 3
                            updateList(heroes, optionNumber, inc = 0.1*Y) # update screen
                        elif event.key == pygame.K_UP:
                            optionNumber = optionNumber - 1 if optionNumber != 3 else 5
                            updateList(heroes, optionNumber, inc = 0.1*Y)  # update screen
                        elif event.key == pygame.K_RETURN:
                            playerhero = heroes[optionNumber]
#                            pygame.event.clear(eventtype=pygame.KEYDOWN)  # https://www.pygame.org/docs/ref/event.html#pygame.event.get
                            if playerhero == "PERCY JACKSON":
                                RoleHero = PercyJackson(playerhero)
                            elif playerhero == "ELF":
                                RoleHero = Elf(playerhero)
                            elif playerhero == "ZELDA":
                                RoleHero = Zelda(playerhero)
                            
                            displayImage(RoleHero.image_name, p=1)
                            wait_til_enter()
                            optionNumber = 0  # set the variable for the next option menu

                            screen.fill(white)
                            pygame_print(text = "Where am I?", loc_y = Y // 1.5, color=black, background_color = white, offset_x=0)
                            pygame.display.update()
                            wait_til_enter()
                            displayImage("treasure_chest.png", p=1)
                            pygame_print(text = "You see a chest.", loc_y = Y // 1.5, color=black, background_color = white, offset_x=0)
                            pygame.display.update()
                            wait_til_enter()
                            displayImage("treasure_chest.png", p=1)
                            pygame_print(text = "Do you open the chest?", loc_y = Y // 1.5, color=black, background_color = white, offset_x=0)
                            pygame.display.update()
                            wait_til_enter()
                            displayImage("treasure_chest.png", p=1)
                            pygame_print(text = "Do you open the chest?", loc_y = Y // 1.5, color=black, background_color = white, offset_x=0)
                            openChestOption(optionNumber)  # Displaying 'Yes' and 'No'
                            dispayedChest = True
#                            pygame.event.clear(eventtype=pygame.KEYDOWN)  # We don't want the enter that they press to do anything until 'Yes' and 'No' are displayed

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

                                #pygame.time.delay(1000)  # Can change later
                                wait_til_enter()

                            screen.fill(white)
                            pygame.display.update()
                            displayedPlaces = True
                            optionNumber = 0

#                        pygame.event.clear(eventtype=pygame.KEYDOWN)  # Clear any keys that were pressed in this if-block

                elif displayedPlaces and not Quests:
                    screen.fill(white)
                    font = pygame.font.Font('freesansbold.ttf', int(0.03733*Y))
                    text = font.render("Where do you want to go?", True, black, white)
                    textRect = text.get_rect()
                    textRect.center = (X // 2, 0.0667*Y)
                    screen.blit(text, textRect)
                    text = font.render("========================", True, black, white)
                    textRect = text.get_rect()
                    textRect.center = (X // 2, 0.12*Y)
                    screen.blit(text, textRect)
                    font = pygame.font.Font('freesansbold.ttf', int(0.0426*Y))
                    PlaceOption(optionNumber)
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
                                #pygame.time.delay(2000)
                                wait_til_enter()
                                Place = House()
                            elif optionNumber == 1:
                                print("Beach")
                                displayImage("StartBeach.png", p=1)
                                #pygame.time.delay(2000)
                                wait_til_enter()
                                Place = Beach()
                            elif optionNumber == 2:
                                print("Forest")
                                displayImage("StartForest.png", p=1)
                                #pygame.time.delay(2000)
                                wait_til_enter()
                                Place = Forest()
                            elif optionNumber == 3:
                                print("Mountain")
                                displayImage("StartMountain.png", p=1)
                                #pygame.time.delay(2000)
                                wait_til_enter()
                                Place = Mountain()
                            elif optionNumber == 4:
                                print("Desert")
                                displayImage("StartDesert.png", p=1)
                                #pygame.time.delay(2000)
                                wait_til_enter()
                                Place = Desert()
#                            pygame.event.clear(eventtype=pygame.KEYDOWN)  # Clear any keys that were pressed in this if-block before displaying the menu
                            Menu(RoleHero, Place)
                            Quests = True
                            pygame.display.update()

                            screen.fill(white)
                            font_sz = int(0.0426*Y)
                            font = pygame.font.Font('freesansbold.ttf', font_sz)
                            pygame_print("New things unlocked!", loc_y = 0.12*Y)
                            pygame.display.update()
                            wait_til_enter()
                            screen.fill(white)
                            font = pygame.font.Font('freesansbold.ttf', font_sz)
                            pygame_print("Quests have been unlocked.", loc_y = 0.12*Y)
                            pygame.display.update()
                            wait_til_enter()
                            screen.fill(white)
                            font = pygame.font.Font('freesansbold.ttf', font_sz)
                            pygame_print("To open quests", loc_y = 0.0933*Y)
                            pygame.display.update()
                            wait_til_enter()
                            screen.fill(white)
                            font = pygame.font.Font('freesansbold.ttf', font_sz)
                            pygame_print("Select 'Quests' in the menu", loc_y = 0.0933*Y)
                            pygame.display.update()
                            wait_til_enter()
#                            pygame.event.clear(eventtype=pygame.KEYDOWN)  # Clear any keys that were pressed in this if-block
                elif Quests:
                    while True:
                        print("hello menu")
                        Menu(RoleHero, Place)

        # Animation

        HeroGame(playerhero)

    except KeyboardInterrupt:
        print("\nBye")
        # TODO: Save Here


game()
