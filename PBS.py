import random
import time
import math
from datetime import datetime
import csv
from shutil import copyfile
import sys


log_output = open("log.txt", "a")
pokemon_stats_sheet = open("Pokemon_Info/pokemon_stats.csv", "r")
leveling_rates_sheet = open("Pokemon_Info/leveling_rates.csv", "r")
moves_sheet = open("Pokemon_Info/Pokemon Moves.csv", "r")

move_used = None
dmg_dealt = None
PlayerPoke1 = None
RivalPoke1 = None
rival_move_used = None
choice = None
playername = None
rivalname = None


def wait(ms):
    time.sleep(ms/1000)

def log(text):
    global log_output
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        log_output.write("{}|     {}\n".format(dt_string, text))
    except:
        log_output.write("{}|     Something went wrong when logging an event.\n".format(dt_string))

def rivalUseMove():
    global rival_move_used
    global dmg_dealt
    global PlayerPoke1
    global RivalPoke1
    global choice
    print("\n{} used {}!".format(RivalPoke1.name, rival_move_used))
    wait(2000)
    if random.randrange(0,100) < int(RivalPoke1.GetMove(rival_move_used)[6]):
        if rival_move_used == "Dragon Rage":
            dmg_dealt = 40
        elif rival_move_used == "Sonic Boom":
            dmg_dealt = 20
        elif rival_move_used == "Fissure" or rival_move_used == "Horn Drill" or rival_move_used == "Guillotine":
            if PlayerPoke1.SPD > RivalPoke1.SPD:
                dmg_dealt = 0
                print("{} evaded the attack!".format(PlayerPoke1.name))
            else:
                dmg_dealt = PlayerPoke1.hp
        elif rival_move_used == "Bide":
            print("Bide is not yet implemented.")
            print("Instead, 10% of {}'s max health will be dealt as damage.".format(PlayerPoke1.name))
            wait(1000)
            dmg_dealt = int(PlayerPoke1.Max_HP / 10)
        elif rival_move_used == "Counter":
            print("Counter is not yet implemented.")
            print("Instead, 10% of {}'s max health will be dealt as damage.".format(PlayerPoke1.name))
            wait(1000)
            dmg_dealt = int(PlayerPoke1.Max_HP / 10)
        elif rival_move_used == "Seismic Toss" or rival_move_used == "Night Shade":
            dmg_dealt = RivalPoke1.level
        elif rival_move_used == "Psywave":
            dmg_dealt = int((random.randint(100,150) / 100) * RivalPoke1.level)
        else:
            try:
                dmg_dealt = RivalPoke1.GetDamage(PlayerPoke1, rival_move_used)
            except:
                print("Something went wrong and the damage coundn't be calculated.")
                print("Please let me know what move you used so I can try to fix it. (Including the log file helps!)")
                print("Instead, 10% of {}'s max health will be dealt as damage.".format(PlayerPoke1.name))
                wait(2000)
                dmg_dealt = int(PlayerPoke1.Max_HP / 10)
                
        RivalPoke1.PP[choice - 1] -= 1
        log("\n\nRival {} attacked".format(RivalPoke1.pokemon))
        log("{}'s health before: {}".format(PlayerPoke1.pokemon, PlayerPoke1.hp))
        PlayerPoke1.hp -= dmg_dealt
        log("{}'s health after: {}".format(PlayerPoke1.pokemon, PlayerPoke1.hp))
        print("\n{} took {} points of damage!".format(PlayerPoke1.name, dmg_dealt))
    else:
        print("\n{} missed!".format(rival_move_used))

def playerUseMove():
    global move_used
    global dmg_dealt
    global PlayerPoke1
    global RivalPoke1
    global choice
    print("\n{} used {}!".format(PlayerPoke1.name, move_used))
    wait(2000)
    if random.randrange(0,100) < int(PlayerPoke1.GetMove(move_used)[6]):
        if move_used == "Dragon Rage":
            dmg_dealt = 40
        elif move_used == "Sonic Boom":
            dmg_dealt = 20
        elif move_used == "Fissure" or move_used == "Horn Drill" or move_used == "Guillotine":
            if RivalPoke1.SPD > PlayerPoke1.SPD:
                dmg_dealt = 0
                print("{} evaded the attack!".format(RivalPoke1.name))
            else:
                dmg_dealt = RivalPoke1.hp
        elif move_used == "Bide":
            print("Bide is not yet implemented.")
            print("As compensation, 10% of {}'s max health will be dealt as damage.".format(RivalPoke1.name))
            wait(1000)
            dmg_dealt = int(RivalPoke1.Max_HP / 10)
        elif move_used == "Counter":
            print("Counter is not yet implemented.")
            print("As compensation, 10% of {}'s max health will be dealt as damage.".format(RivalPoke1.name))
            wait(1000)
            dmg_dealt = int(RivalPoke1.Max_HP / 10)
        elif move_used == "Seismic Toss" or move_used == "Night Shade":
            dmg_dealt = PlayerPoke1.level
        elif move_used == "Psywave":
            dmg_dealt = int((random.random(100,150) / 100) * PlayerPoke1.level)
        else:
            try:
                dmg_dealt = PlayerPoke1.GetDamage(RivalPoke1, move_used)
            except:
                print("Something went wrong and the damage coundn't be calculated.")
                print("Please let me know what move you used so I can try to fix it. (Including the log file helps!)")
                print("As compensation, 10% of {}'s max health will be dealt as damage.".format(RivalPoke1.name))
                wait(2000)
                dmg_dealt = int(RivalPoke1.Max_HP / 10)
                
                
        PlayerPoke1.PP[choice - 1] -= 1
        log("\n\n{} attacked".format(PlayerPoke1.pokemon))
        log("{}'s health before: {}".format(RivalPoke1.pokemon, RivalPoke1.hp))
        RivalPoke1.hp -= dmg_dealt
        log("{}'s health after: {}".format(RivalPoke1.pokemon, RivalPoke1.hp))
        print("\nRival {} took {} points of damage!".format(RivalPoke1.name, dmg_dealt))
    else:
        print("\n{} missed!".format(move_used))

def addZeroes(num, zeroes):
    word = str(num)
    before = [i for i in word]
    if len(before) < zeroes:
        for i in range(zeroes - len(before)):
            before.insert(0, "0")
    after = "".join(before)
    return after

def addWhitespace(txt, length):
    word = str(txt)
    before = [i for i in word]
    if len(before) < length:
        for i in range(length - len(before)):
            before.append(" ")
    after = "".join(before)
    return after

def getPercentages(poke1, poke2):
    ans = (math.floor(poke1.hp / poke1.Max_HP * 100), math.floor(poke2.hp / poke2.Max_HP * 100))
    return ans

def getHealthBars(poke1, poke2):
    health1, health2 = getPercentages(poke1, poke2)
    p1 = int(health1 / 10)
    p2 = int(health2 / 10)
    p1final = []
    p2final = []
    for i in range(p1):
        p1final.append("#")
    for i in range(p2):
        p2final.append("#")
    for i in range(10 - len(p1final)):
        p1final.append("-")
    for i in range(10 - len(p2final)):
        p2final.append("-")
    return("".join(p1final),"".join(p2final))

def askForNumber(phrase):
    try:
        return(int(input(phrase)))
    except:
        print("Something went wrong. Please try again.")
        print("")
        askForNumber(phrase)
        
def askForLimitedNumber(phrase, mn, mx):
    x = None
    try:
        x = (int(input(phrase)))
        if x < mn or x > mx:
            print("Please enter a number between {} and {}.".format(mn, mx))
            print("")
            return(askForLimitedNumber(phrase, mn, mx))
        else:
            return(x)
    except:
        print("Something went wrong. Please try again.")
        print("")
        return(askForLimitedNumber(phrase, mn, mx))
   

        


def askList(phrase, aa):
    x = input(phrase)
    if not x in aa:
        while True:
            print("\nInvalid answer.")
            print("Allowed answers are:")
            print(aa)
            print("")
            x = input(phrase)
            if x in aa:
                return(x)
    else:
        return(x)


otherlist = []
pokemon_stats = []
leveling_rates = []
allMoves = []
leveling_dict = {'Fast':2, 'Medium Fast':3, 'Medium Slow':4, 'Slow':5}

for line in pokemon_stats_sheet.readlines():
    otherlist.append(line.replace('\n', ''))
for pokemon in otherlist:
    pokemon_stats.append(pokemon.split(','))

otherlist = []

for line in leveling_rates_sheet.readlines():
    otherlist.append(line.replace('\n', ''))
for level in otherlist:
    leveling_rates.append(level.split(','))
    
otherlist = []

specialTypes = ['Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark']
physicalTypes = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel']


#Hop approves
#StrongAgainst: deals 2x damage to anyone in that list
#WeakAgainst: deals 0.5x damag to anyone in that list
#IneffectiveAgainst: deals 0x damage to anyone in this list
type_matchups = {'Normal':{'StrongAgainst':[], 'WeakAgainst':['Rock', 'Steel'], 'IneffectiveAgainst':['Ghost']}, 'Fire':{'StrongAgainst':['Grass', 'Ice', 'Bug', 'Steel'], 'WeakAgainst':['Fire', 'Water', 'Rock', 'Dragon'], 'IneffectiveAgainst':[]}, 'Water':{'StrongAgainst':['Fire', 'Ground', 'Rock'], 'WeakAgainst':['Water', 'Grass', 'Dragon'], 'IneffectiveAgainst':[]}, 'Grass':{'StrongAgainst':['Water', 'Ground', 'Rock'], 'WeakAgainst':['Fire', 'Grass', 'Poison', 'Flying', 'Bug', 'Dragon', 'Steel'], 'IneffectiveAgainst':[]}, 'Electric':{'StrongAgainst':['Water', 'Flying'], 'WeakAgainst':['Grass', 'Electric', 'Dragon'], 'IneffectiveAgainst':['Ground']}, 'Ice':{'StrongAgainst':['Grass', 'Ground', 'Flying', 'Dragon'], 'WeakAgainst':['Fire', 'Water', 'Ice', 'Steel'], 'IneffectiveAgainst':[]}, 'Fighting':{'StrongAgainst':['Normal', 'Ice', 'Rock', 'Dark', 'Steel'], 'WeakAgainst':['Poison', 'Flying', 'Psychic', 'Bug', 'Fairy'], 'IneffectiveAgainst':['Ghost']}, 'Poison': {'StrongAgainst':['Grass', 'Fairy'], 'WeakAgainst':['Poison', 'Ground', 'Rock', 'Ghost'], 'IneffectiveAgainst':['Steel']}, 'Ground': {'StrongAgainst':['Fire', 'Electric', 'Poison', 'Rock', 'Steel'], 'WeakAgainst':['Grass', 'Bug'], 'IneffectiveAgainst':['Flying']}, 'Flying': {'StrongAgainst':['Grass', 'Fighting', 'Bug'], 'WeakAgainst':['Electrc', 'Rock', 'Steel'], 'IneffectiveAgainst':[]}, 'Psychic': {'StrongAgainst':['Fighting', 'Poison'], 'WeakAgainst':['Psychic', 'Steel'], 'IneffectiveAgainst':['Dark']}, 'Bug': {'StrongAgainst':['Grass', 'Psychic', 'Dark'], 'WeakAgainst':['Fire', 'Fighting', 'Poison', 'Flying', 'Dark', 'Steel', 'Fairy'], 'IneffectiveAgainst':[]}, 'Rock': {'StrongAgainst':['Fire', 'Ice', 'Flying', 'Bug'], 'WeakAgainst':['Fighting', 'Ground', 'Steel'], 'IneffectiveAgainst':[]}, 'Ghost': {'StrongAgainst':['Ghost', 'Psychic'], 'WeakAgainst':['Dark'], 'IneffectiveAgainst':['Normal']}, 'Dragon': {'StrongAgainst':['Dragon'], 'WeakAgainst':['Steel'], 'IneffectiveAgainst':['Fairy']}, 'Dark': {'StrongAgainst':['Psychic', 'Ghost'], 'WeakAgainst':['Fighting', 'Fairy'], 'IneffectiveAgainst':[]}, 'Steel': {'StrongAgainst':['Ice', 'Rock', 'Fairy'], 'WeakAgainst':['Fire', 'Water', 'Electric', 'Steel'], 'IneffectiveAgainst':[]}, 'Fairy': {'StrongAgainst':['Fighting', 'Dragon', 'Dark'], 'WeakAgainst':['Fire', 'Steel'], 'IneffectiveAgainst':[]}}

for line in moves_sheet.readlines():
    otherlist.append(line.replace('\n', ''))
for move in otherlist:
    allMoves.append(move.split(','))

def getStat(pokemon, stat_location):
    for monster in pokemon_stats:
        if pokemon in monster:
            return monster[stat_location]


class Pokemon:
    def __init__(self, name='RATTATA', p_type=['normal'], pokemon='Rattata', level=5, hp=True):
        self.moves = []
        self.PP = []
        self.name = name
        self.level = level
        if self.level > 100:
            self.level = 100
        elif self.level < 1:
            self.level = 1
        self.hp = hp
        self.pokemon = pokemon
        self.p_type = (p_type)
        
        #Alright, now for the other variables
        if int(getStat(self.pokemon, 2)) == 1:
            self.stage = 'basic'
        else:
            self.stage = 'stage ' + getStat(self.pokemon, 2)
        self.number = int(getStat(self.pokemon, 0))
        self.Base_HP = int(getStat(self.pokemon, 3))
        self.Base_ATK = int(getStat(self.pokemon, 4))
        self.Base_DEF = int(getStat(self.pokemon, 5))
        self.Base_SPD = int(getStat(self.pokemon, 6))
        self.Base_Sp = int(getStat(self.pokemon, 7))
        self.leveling_rate = (getStat(self.pokemon, 8))
        #self.Until_next_level = None
        #for line in leveling_rates:
        #    if str(self.level) in line:
        #        self.Until_next_level = int(line[leveling_dict[self.leveling_rate]]) - self.xp
        #if self.xp > self.Until_next_level:
        #    self.xp = self.Until_next_level - 1
        self.HP_EV = 0
        self.ATK_EV = 0
        self.DEF_EV = 0
        self.SPD_EV = 0
        self.Sp_EV = 0
        #self.award_EV = ('SPD', 1) uneeded in this project
        self.HP_IV = 0
        self.ATK_IV = random.randint(0, 15)
        self.DEF_IV = random.randint(0, 15)
        self.SPD_IV = random.randint(0, 15)
        self.Sp_IV = random.randint(0, 15)
        if self.ATK_IV%2 == 1:
            self.HP_IV += 8
        if self.DEF_IV%2 == 1:
            self.HP_IV += 4
        if self.SPD_IV%2 == 1:
            self.HP_IV += 2
        if self.Sp_IV%2 == 1:
            self.HP_IV += 1
        self.Max_HP = round((((self.Base_HP + self.HP_IV)*2 +(self.HP_EV/4) * self.level)/100) + self.level + 10)
        self.ATK = (((self.Base_ATK + self.ATK_IV)*2 +(self.ATK_EV/4) * self.level)/100) + 5
        self.DEF = (((self.Base_DEF + self.DEF_IV)*2 +(self.DEF_EV/4) * self.level)/100) + 5
        self.SPD = (((self.Base_SPD + self.SPD_IV)*2 +(self.SPD_EV/4) * self.level)/100) + 5
        self.Sp = (((self.Base_Sp + self.Sp_IV)*2 +(self.Sp_EV/4) * self.level)/100) + 5
        if self.hp == True:
            self.hp = self.Max_HP
        if self.hp > self.Max_HP:
            self.hp = self.Max_HP
  
    def __str__(self):
            try:
                return "{} is a {} {}\n({}/{} Pokemon) at level {}.\nHP: {}/{}.".format(self.name, self.stage, self.pokemon, self.p_type[0], self.p_type[1], self.level, self.hp, self.Max_HP)
            except:
                return "{} is a {} {}\n({} Pokemon) at level {}.\nHP: {}/{}.".format(self.name, self.stage, self.pokemon, self.p_type[0], self.level, self.hp, self.Max_HP)
    
    def UpdateStats(self):
        self.Max_HP = round((((self.Base_HP + self.HP_IV)*2 +(self.HP_EV/4) * self.level)/100) + self.level + 10)
        self.ATK = (((self.Base_ATK + self.ATK_IV)*2 +(self.ATK_EV/4) * self.level)/100) + 5
        self.DEF = (((self.Base_DEF + self.DEF_IV)*2 +(self.DEF_EV/4) * self.level)/100) + 5
        self.SPD = (((self.Base_SPD + self.SPD_IV)*2 +(self.SPD_EV/4) * self.level)/100) + 5
        self.Sp = (((self.Base_Sp + self.Sp_IV)*2 +(self.Sp_EV/4) * self.level)/100) + 5
    def GetStrongAgainst(self):
        return type_matchups[self.p_type][StrongAgainst]
    def GetWeakAgainst(self):
        return type_matchups[self.p_type][WeakAgainst]
    def GetIneffectiveAgainst(self):
        return type_matchups[self.p_type][IneffectiveAgainst]
    def Level_up(self):
        self.level += 1
        self.Base_HP += ((self.Base_HP/50) + ((self.HP_IV + self.HP_EV)/100))
        self.Base_ATK += ((self.Base_ATK/50) + ((self.ATK_EV + self.ATK_EV)/100))
        self.Base_DEF += ((self.Base_DEF/50) + ((self.DEF_IV + self.DEF_EV)/100))
        self.Base_SPD += ((self.Base_SPD/50) + ((self.SPD_IV + self.SPD_EV)/100))
        self.Base_Sp += ((self.Base_Sp/50) + ((self.Sp_IV + self.Sp_EV)/100))
    def Evolve(self):
        pass
    def GetMove(self, i):
        for move in allMoves:
            if move[1] == i:
                return move
    def GetDamage(self, opponent, move):
        log("\n\ncalculating damage of {} using {} on {}".format(self.pokemon, move, opponent.pokemon))
        if (self.GetMove(move))[2] == 'Status':
            log("{} is a status move".format(move))
            return('Status Move')
        elif (self.GetMove(move))[2] == 'Physical':
            A = int(self.ATK)
            log("A = {}".format(A))
            D = int(opponent.DEF)
            log("D = {}".format(D))
            Power = (self.GetMove(move))[5]
            log("Power = {}".format(Power))
            Random = (random.randint(217, 256)) / 255
            log("Random = {}".format(Random))
            if (self.GetMove(move))[2] in self.p_type:
                STAB = 1.5
                log("STAB = 1.5")
            else:
                STAB = 1
                log("STAB = 1")
            if opponent.p_type[0] in type_matchups[(self.GetMove(move))[2]]['StrongAgainst'] or opponent.p_type[-1] in type_matchups[(self.GetMove(move))[2]]['StrongAgainst']:
                TypeBonus = 2
                log("TypeBonus = 2")
            elif opponent.p_type[0] in type_matchups[(self.GetMove(move))[2]]['WeakAgainst'] or opponent.p_type[-1] in type_matchups[(self.GetMove(move))[2]]['WeakAgainst']:
                TypeBonus = 0.5
                log("TypeBonus = 0.5")
            elif opponent.p_type[0] in type_matchups[(self.GetMove(move))[2]]['IneffectiveAgainst'] or opponent.p_type[-1] in type_matchups[(self.GetMove(move))[2]]['IneffectiveAgainst']:
                TypeBonus = 0
                log("TypeBonus = 0")
            else:
                TypeBonus = 1
                log("TypeBonus = 1")
            
            log("level = {}".format(self.level))
            log("var1 = 2 * level = {}".format(2*self.level))
            var1 = 2*self.level
            log("var2 = var1 / 5 = {}".format(var1 / 5))
            var2 = var1 / 5
            log("var3 = var2 + 2 ~= {}".format(int(var2 + 2)))
            var3 = int(var2 + 2)
            log("var4 = var3 * Power = {}".format(var3 * int(Power)))
            var4 = var3 * int(Power)
            log("var5 = A / D ~= {}".format(A/D))
            var5 = A/D
            log("var6 = var4 * var5 = {}".format(var4*var5))
            var6 = var4*var5
            log("var7 = var6 / 50 = {}".format(var6/50))
            var7 = var6/50
            log("var8 = var7 + 2 = {}".format(var7 + 2))
            var8 = var7 + 2
            log("var9 = var8 * TypeBonus = {}".format(var8 * TypeBonus))
            var9 = var8 * TypeBonus
            log("var10 = var9 * STAB = {}".format(var9 * STAB))
            var10 = var9 * STAB
            log("var11 = var10 * Random = {}".format(Var10 * Random))
            var11 = var10 * Random
            log("var12 = var11 rounded = {}".format(int(var11)))
            var12 = int(var11)
            log("var12 = {}".format(var12))
            
                
            log("Total damage: {}".format(int((((int((((2*self.level) / 5) + 2)) * int(Power) * (A / D)) / 50) + 2) * TypeBonus * STAB * Random)))
            return(int((((int((((2*self.level) / 5) + 2)) * int(Power) * (A / D)) / 50) + 2) * TypeBonus * STAB * Random))
        
        else:
            A = int(self.Sp)
            log("A = {}".format(A))
            D = int(opponent.Sp)
            log("D = {}".format(D))
            Power = (self.GetMove(move))[5]
            log("Power = {}".format(Power))
            Random = (random.randint(217, 256)) / 255
            log("Random = {}".format(Random))
            if (self.GetMove(move))[2] in self.p_type:
                STAB = 1.5
                log("STAB = 1.5")
            else:
                STAB = 1
                log("STAB = 1")
            if opponent.p_type[0] in type_matchups[(self.GetMove(move))[2]]['StrongAgainst'] or opponent.p_type[-1] in type_matchups[(self.GetMove(move))[2]]['StrongAgainst']:
                TypeBonus = 2
                log("TypeBonus = 2")
            elif opponent.p_type[0] in type_matchups[(self.GetMove(move))[2]]['WeakAgainst'] or opponent.p_type[-1] in type_matchups[(self.GetMove(move))[2]]['WeakAgainst']:
                TypeBonus = 0.5
                log("TypeBonus = 0.5")
            elif opponent.p_type[0] in type_matchups[(self.GetMove(move))[2]]['IneffectiveAgainst'] or opponent.p_type[-1] in type_matchups[(self.GetMove(move))[2]]['IneffectiveAgainst']:
                TypeBonus = 0
                log("TypeBonus = 0")
            else:
                TypeBonus = 1
                log("TypeBonus = 1")
                
            log("level = {}".format(self.level))
            log("var1 = 2 * level = {}".format(2*self.level))
            var1 = 2*self.level
            log("var2 = var1 / 5 = {}".format(var1 / 5))
            var2 = var1 / 5
            log("var3 = var2 + 2 ~= {}".format(int(var2 + 2)))
            var3 = int(var2 + 2)
            log("var4 = var3 * Power = {}".format(var3 * int(Power)))
            var4 = var3 * int(Power)
            log("var5 = A / D ~= {}".format(A/D))
            var5 = A/D
            log("var6 = var4 * var5 = {}".format(var4*var5))
            var6 = var4*var5
            log("var7 = var6 / 50 = {}".format(int(var6)/50))
            var7 = int(var6)/50
            log("var8 = var7 + 2 = {}".format(var7 + 2))
            var8 = var7 + 2
            log("var9 = var8 * TypeBonus = {}".format(var8 * TypeBonus))
            var9 = var8 * TypeBonus
            log("var10 = var9 * STAB = {}".format(var9 * STAB))
            var10 = var9 * STAB
            log("var11 = var10 * Random = {}".format(var10 * Random))
            var11 = var10 * Random
            log("var12 = var11 rounded = {}".format(int(var11)))
            var12 = int(var11)
            log("var12 = {}".format(var12))
                
            log("Total damage: {}".format(int((((int((((2*self.level) / 5) + 2)) * int(Power) * (A / D)) / 50) + 2) * TypeBonus * STAB * Random)))
            return(int((((int((((2*self.level) / 5) + 2)) * int(Power) * (A / D)) / 50) + 2) * TypeBonus * STAB * Random))

        
        
        
        
        
        
        
        
otherlist = []



def getInfoFromSave():
    global otherlist
    global playername
    global rivalname
    global PlayerPoke1
    global RivalPoke1
    save_file = open("Saves/save.txt", "r")
    savedata = []
    
    for line in save_file.readlines():
        otherlist.append(line.replace('\n', ''))
    for i in otherlist:
        savedata.append(i.split(','))
    save_file.close()
            
    print("\nLoading save....\n")
    playername = savedata[0][0]
    print("Player name: {}".format(playername))
    rivalname = savedata[1][0]
    print("Rival name: {}".format(rivalname))
    
    
    
    if savedata[2][4] == "None":
        PlayerPoke1 = Pokemon(name=savedata[2][0], p_type=[savedata[2][3]], pokemon=savedata[2][1], level=int(savedata[2][2]), hp=int(savedata[2][19]))
    else:
        PlayerPoke1 = Pokemon(name=savedata[2][0], p_type=[savedata[2][3], savedata[2][4]], pokemon=savedata[2][1], level=int(savedata[2][2]), hp=int(savedata[2][19]))

    PlayerPoke1.HP_EV = int(savedata[2][9])
    PlayerPoke1.ATK_EV = int(savedata[2][10])
    PlayerPoke1.DEF_EV = int(savedata[2][11])
    PlayerPoke1.SPD_EV = int(savedata[2][12])
    PlayerPoke1.Sp_EV = int(savedata[2][13])
    PlayerPoke1.HP_IV = int(savedata[2][14])
    PlayerPoke1.ATK_IV = int(savedata[2][15])
    PlayerPoke1.DEF_IV = int(savedata[2][16])
    PlayerPoke1.SPD_IV = int(savedata[2][17])
    PlayerPoke1.Sp_IV = int(savedata[2][18])
    PlayerPoke1.UpdateStats()
    PlayerPoke1.hp = int(savedata[2][19])
    PlayerPoke1.moves = savedata[2][5:9]
    PlayerPoke1.PP = [int(PlayerPoke1.GetMove(i)[4]) for i in PlayerPoke1.moves]
    
    print("{}'s Pokemon: {} the level {} {}.".format(playername, PlayerPoke1.name, PlayerPoke1.level, PlayerPoke1.pokemon))
    
    
    if savedata[3][4] == "None":
        RivalPoke1 = Pokemon(name=savedata[3][0], p_type=[savedata[3][3]], pokemon=savedata[3][1], level=int(savedata[3][2]), hp=int(savedata[3][19]))
    else:
        RivalPoke1 = Pokemon(name=savedata[3][0], p_type=[savedata[3][3], savedata[3][4]], pokemon=savedata[3][1], level=int(savedata[3][2]), hp=int(savedata[3][19]))
        
    RivalPoke1.HP_EV = int(savedata[3][9])
    RivalPoke1.ATK_EV = int(savedata[3][10])
    RivalPoke1.DEF_EV = int(savedata[3][11])
    RivalPoke1.SPD_EV = int(savedata[3][12])
    RivalPoke1.Sp_EV = int(savedata[3][13])
    RivalPoke1.HP_IV = int(savedata[3][14])
    RivalPoke1.ATK_IV = int(savedata[3][15])
    RivalPoke1.DEF_IV = int(savedata[3][16])
    RivalPoke1.SPD_IV = int(savedata[3][17])
    RivalPoke1.Sp_IV = int(savedata[3][18])
    RivalPoke1.UpdateStats()
    RivalPoke1.hp = int(savedata[3][19])
    RivalPoke1.moves = savedata[3][5:9]
    RivalPoke1.PP = [int(RivalPoke1.GetMove(i)[4]) for i in RivalPoke1.moves]
        
    print("{}'s Pokemon: {} the level {} {}.".format(rivalname, RivalPoke1.name, RivalPoke1.level, RivalPoke1.pokemon))
    print("\nSave loaded!\n")
    log("\n\nSave file loaded. {} vs rival {}.".format(PlayerPoke1.name, RivalPoke1.name))
    input("Type anything to continue ")

def makeNewPokemon():
    global otherlist
    global playername
    global rivalname
    global PlayerPoke1
    global RivalPoke1
    print("Hello there, Trainer!")
    wait(1000)
    print("Welcome to the Pokemon Battle Simulator!")
    wait(1000)
    print("Here you'll be able to set up a fight between two Pokemon, one of which you control.")
    wait(1000)
    print("Currently this is a work in progress, and I'll do my best to improve it over time.")
    wait(1000)
    print("Disclaimer: I do not own the rights to Pokemon, this is but a fan made game. All copyrights belong to their respective owners.")
    wait(1000)
    answer = input("Type anything to continue. ")
    print("\nA note for Pokenerds: This game is set, to the best of my ability, in Generation 1, with all of it's implications.")
    answer = input("Type anything to continue. Pokenerds: Type \"info\" for details. ")
    if answer == "info":
        print("\nWhen prompted to enter a number referencing a Pokemon, check \"pokemon_stats.csv\" for a list of Pokemon.\n")
        print("When prompted to enter a number referencing a move, check \"Pokemon Moves.csv\" for a list of moves.\n")
        print("In Gen I, both Sp. ATK and Sp. DEF are controlled by the single Special stat, not individual stats.\nThis game also has that mechanic implemented. I recommend checking the Bulbapedia periodically.\n")
        print("As in Gen I, all moves that are 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', or 'Dark' type are considered\nspecial, and all other types are physical.\n")
        print("Currnenly, all EVs are set to 0 and cannot be increased.\n")
        print("IVs are randomized, using the traditional Pokemon IV randomization.\n")
        print("In the future, EVs and IVs may be able to be customized.\n")
        print("There is no Pokerus and there are no shinies.\n")
        print("Currently, Status moves and Abilities are not yet implemented. They will not do anything.\n")
        print("IMPORTANT NOTE!! This game uses the EV calculations of Gen 3,\nas in Generations 1 and 2, the EV system was kinda off kilter. There is no EV gain from battles\nin this game.\n")
        answer = input("Type anything to continute. ")
    print("")
    print("Let's begin.")
    wait(1000)
    playername = input("What is your name? ")
    print("Hello, {}.".format(playername))
    wait(500)
    print("Start off by entering the number of the Pokemon YOU want to battle WITH.")
    number = askForLimitedNumber("Enter a number: ", 1, 151)
    PokeSpecies = pokemon_stats[number - 1][1]
    print("You chose {}.".format(PokeSpecies))
    if askList("Give it a nickname? ", ["yes","no"]) == "yes":
        PokeName = input("Give {} a name: ".format(PokeSpecies))
    else:
        PokeName = PokeSpecies.upper()
    print("")
    print("Say hi to {} the {}!".format(PokeName, PokeSpecies))
    wait(2000)
    print("<{}> Hi {}!\n".format(playername, PokeName))
    wait(2000)
    Type1 = askList("Currently, {}'s type cannot be determined by the program.\nEnter {}'s type (you can change it if you want!)\nIf {} is dual-type, enter the first type: ".format(PokeName, PokeName, PokeName), ['Bug', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Water'])
    Type2 = askList("If {} has a second type, enter it now. Otherwise, type \"None\". ".format(PokeName), ['Bug', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Water', 'None'])
    PokeLevel = askForLimitedNumber("\nEnter {}'s level: ".format(PokeName), 1, 100)
    if Type2 == "None":
        print("{} the {} is a {} Pokemon at level {}.\n".format(PokeName, PokeSpecies, Type1, PokeLevel))
    else:
        print("{} the {} is a {}/{} Pokemon at level {}.\n".format(PokeName, PokeSpecies, Type1, Type2, PokeLevel))
    
    
    if Type2 == "None":
        PlayerPoke1 = Pokemon(name=PokeName, p_type=[Type1], pokemon=PokeSpecies, level=PokeLevel, hp=True)
    else:
        PlayerPoke1 = Pokemon(name=PokeName, p_type=[Type1, Type2], pokemon=PokeSpecies, level=PokeLevel, hp=True)

    if askList("{}'s EVs are currently all 0. You can customize this.\nWould you like to set {}'s EVs? (I reccomend only doing this if you know what you're doing!) ".format(PlayerPoke1.name, PlayerPoke1.name), ["yes", "no"]) == "yes":
        EV1 = askForLimitedNumber("Enter {}'s HP EV: ".format(PokeName), 0, 252)
        EV2 = askForLimitedNumber("Enter {}'s ATK EV: ".format(PokeName), 0, 252)
        EV3 = askForLimitedNumber("Enter {}'s DEF EV: ".format(PokeName), 0, 252)
        EV4 = askForLimitedNumber("Enter {}'s SPD EV: ".format(PokeName), 0, 252)
        EV5 = askForLimitedNumber("Enter {}'s Sp EV: ".format(PokeName), 0, 252)
        PlayerPoke1.HP_EV = EV1
        PlayerPoke1.ATK_EV = EV2
        PlayerPoke1.DEF_EV = EV3
        PlayerPoke1.SPD_EV = EV4
        PlayerPoke1.Sp_EV = EV1
        print("EVs for {} sucessuflly changed.".format(PlayerPoke1.name))
    else:
        EV1 = 0
        EV2 = 0
        EV3 = 0
        EV4 = 0
        EV5 = 0
        PlayerPoke1.HP_EV = EV1
        PlayerPoke1.ATK_EV = EV2
        PlayerPoke1.DEF_EV = EV3
        PlayerPoke1.SPD_EV = EV4
        PlayerPoke1.Sp_EV = EV1

    if askList("\n{}'s IVs are currently all randomized. You can customize this.\nWould you like to set {}'s IVs? (I *really* reccomend only doing this if you know what you're doing!) ".format(PlayerPoke1.name, PlayerPoke1.name), ["yes", "no"]) == "yes":
        IV1 = askForLimitedNumber("Enter {}'s HP IV: ".format(PokeName), 0, 15)
        IV2 = askForLimitedNumber("Enter {}'s ATK IV: ".format(PokeName), 0, 15)
        IV3 = askForLimitedNumber("Enter {}'s DEF IV: ".format(PokeName), 0, 15)
        IV4 = askForLimitedNumber("Enter {}'s SPD IV: ".format(PokeName), 0, 15)
        IV5 = askForLimitedNumber("Enter {}'s Sp IV: ".format(PokeName), 0, 15)
        PlayerPoke1.HP_IV = IV1
        PlayerPoke1.ATK_IV = IV2
        PlayerPoke1.DEF_IV = IV3
        PlayerPoke1.SPD_IV = IV4
        PlayerPoke1.Sp_IV = IV1
        print("IVs sucessfully set.")
        
        
    PlayerPoke1.UpdateStats()
    print("\n{} has {} max health.".format(PlayerPoke1.name, PlayerPoke1.Max_HP))
    if askList("Would you like to set {}'s HP to something othen than maximum? ".format(PlayerPoke1.name),["yes", "no"]) == "yes":
        PlayerPoke1.hp = askForLimitedNumber("Enter new HP: ", 1, PlayerPoke1.Max_HP)
    else:
        PlayerPoke1.hp = PlayerPoke1.Max_HP
    print("")
    print("Almost done!")
    wait(1000)
    print("Now it's time to give {} some moves".format(PlayerPoke1.name))
    for i in range(askForLimitedNumber("{} can learn up to 4 moves. How many moves do you want to teach {}? ".format(PlayerPoke1.name, PlayerPoke1.name),1,4)):
        number = askForLimitedNumber("Enter a move number: ",1,165)
        if (PlayerPoke1.GetMove((allMoves[number][1])))[3] == 'Status':
            while True:
                print(allMoves[number][1] + " is a status move and as such is currently unimplemented. Please choose another move.")
                number = askForLimitedNumber("Enter a move number: ",1,165)
                if not((PlayerPoke1.GetMove((allMoves[number][1])))[3] == 'Status'):
                    break
        print(allMoves[number][1])
        print("")
        PlayerPoke1.moves.append(allMoves[number][1])
    while len(PlayerPoke1.moves) < 4:
        PlayerPoke1.moves.append("None")
    print("{}'s moveset: {}, {}, {}, and {}.\n".format(PlayerPoke1.name, PlayerPoke1.moves[0], PlayerPoke1.moves[1], PlayerPoke1.moves[2], PlayerPoke1.moves[3]))

    PlayerPoke1.PP = [int(PlayerPoke1.GetMove(i)[4]) for i in PlayerPoke1.moves]
    print("All done setting up your Pokemon!")
    wait(1000)
    print("\n\n")
    print("Now, it's time to set up your opponent's Pokemon! The proccess will be identical to the one you just did.")






    rivalname = input("Enter your rival's name: ")
    wait(500)
    print("Start off by entering the number of the Pokemon YOU want to battle AGAINST.")
    number = askForLimitedNumber("Enter a number: ", 1, 151)
    PokeSpecies = pokemon_stats[number - 1][1]
    print("You chose {}.".format(PokeSpecies))
    if askList("Give it a nickname? ", ["yes","no"]) == "yes":
        PokeName = input("Give {} a name: ".format(PokeSpecies))
    else:
        PokeName = PokeSpecies.upper()
    print("")
    print("{}, say hi to {} the {}!".format(rivalname, PokeName, PokeSpecies))
    wait(2000)
    print("<{}> Hi {}!\n".format(rivalname, PokeName))
    wait(2000)
    Type1 = askList("Currently, {}'s type cannot be determined by the program.\nEnter {}'s type (you can change it if you want!)\nIf {} is dual-type, enter the first type: ".format(PokeName, PokeName, PokeName), ['Bug', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Water'])
    Type2 = askList("If {} has a second type, enter it now. Otherwise, type \"None\". ".format(PokeName), ['Bug', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Water', 'None'])
    PokeLevel = askForLimitedNumber("\nEnter {}'s level: ".format(PokeName), 1, 100)
    if Type2 == "None":
        print("{} the {} is a {} Pokemon at level {}.\n".format(PokeName, PokeSpecies, Type1, PokeLevel))
    else:
        print("{} the {} is a {}/{} Pokemon at level {}.\n".format(PokeName, PokeSpecies, Type1, Type2, PokeLevel))
        
        
    if Type2 == "None":
        RivalPoke1 = Pokemon(name=PokeName, p_type=[Type1], pokemon=PokeSpecies, level=PokeLevel, hp=True)
    else:
        RivalPoke1 = Pokemon(name=PokeName, p_type=[Type1, Type2], pokemon=PokeSpecies, level=PokeLevel, hp=True)
    
    if askList("{}'s EVs are currently all 0. You can customize this.\nWould you like to set {}'s EVs? (I reccomend only doing this if you know what you're doing!) ".format(RivalPoke1.name, RivalPoke1.name), ["yes", "no"]) == "yes":
        EV1 = askForLimitedNumber("Enter {}'s HP EV: ".format(PokeName), 0, 252)
        EV2 = askForLimitedNumber("Enter {}'s ATK EV: ".format(PokeName), 0, 252)
        EV3 = askForLimitedNumber("Enter {}'s DEF EV: ".format(PokeName), 0, 252)
        EV4 = askForLimitedNumber("Enter {}'s SPD EV: ".format(PokeName), 0, 252)
        EV5 = askForLimitedNumber("Enter {}'s Sp EV: ".format(PokeName), 0, 252)
        RivalPoke1.HP_EV = EV1
        RivalPoke1.ATK_EV = EV2
        RivalPoke1.DEF_EV = EV3
        RivalPoke1.SPD_EV = EV4
        RivalPoke1.Sp_EV = EV1
        print("EVs for {} sucessuflly changed.".format(RivalPoke1.name))
    else:
        EV1 = 0
        EV2 = 0
        EV3 = 0
        EV4 = 0
        EV5 = 0
        RivalPoke1.HP_EV = EV1
        RivalPoke1.ATK_EV = EV2
        RivalPoke1.DEF_EV = EV3
        RivalPoke1.SPD_EV = EV4
        RivalPoke1.Sp_EV = EV1
    
    if askList("\n{}'s IVs are currently all randomized. You can customize this.\nWould you like to set {}'s IVs? (I *really* reccomend only doing this if you know what you're doing!) ".format(RivalPoke1.name, RivalPoke1.name), ["yes", "no"]) == "yes":
        IV1 = askForLimitedNumber("Enter {}'s HP IV: ".format(PokeName), 0, 15)
        IV2 = askForLimitedNumber("Enter {}'s ATK IV: ".format(PokeName), 0, 15)
        IV3 = askForLimitedNumber("Enter {}'s DEF IV: ".format(PokeName), 0, 15)
        IV4 = askForLimitedNumber("Enter {}'s SPD IV: ".format(PokeName), 0, 15)
        IV5 = askForLimitedNumber("Enter {}'s Sp IV: ".format(PokeName), 0, 15)
        RivalPoke1.HP_IV = IV1
        RivalPoke1.ATK_IV = IV2
        RivalPoke1.DEF_IV = IV3
        RivalPoke1.SPD_IV = IV4
        RivalPoke1.Sp_IV = IV1
        print("IVs sucessfully set.")
        
    
    
    
    RivalPoke1.UpdateStats()
    print("\n{} has {} max health.".format(RivalPoke1.name, RivalPoke1.Max_HP))
    if askList("Would you like to set {}'s HP to something othen than maximum? ".format(RivalPoke1.name),["yes", "no"]) == "yes":
        RivalPoke1.hp = askForLimitedNumber("Enter new HP: ", 1, RivalPoke1.Max_HP)
    else:
        RivalPoke1.hp = RivalPoke1.Max_HP
    print("")
    print("Almost done!")
    wait(1000)
    print("Now it's time to give {} some moves".format(RivalPoke1.name))
    for i in range(askForLimitedNumber("{} can learn up to 4 moves. How many moves do you want to teach {}? ".format(RivalPoke1.name, RivalPoke1.name),1,4)):
        number = askForLimitedNumber("Enter a move number: ",1,165)
        if (RivalPoke1.GetMove((allMoves[number][1])))[3] == 'Status':
            while True:
                print(allMoves[number][1] + " is a status move and as such is currently unimplemented. Please choose another move.")
                number = askForLimitedNumber("Enter a move number: ",1,165)
                if not((RivalPoke1.GetMove((allMoves[number][1])))[3] == 'Status'):
                    break
        print(allMoves[number][1])
        print("")
        RivalPoke1.moves.append(allMoves[number][1])
    while len(RivalPoke1.moves) < 4:
        RivalPoke1.moves.append("None")
    print("{}'s moveset: {}, {}, {}, and {}.\n".format(RivalPoke1.name, RivalPoke1.moves[0], RivalPoke1.moves[1], RivalPoke1.moves[2], RivalPoke1.moves[3]))


    RivalPoke1.PP = [int(RivalPoke1.GetMove(i)[4]) for i in RivalPoke1.moves]
    print("All done setting up your rival's Pokemon!\n\n\n")
    wait(1000)

def battle():
    global PlayerPoke1
    global RivalPoke1
    global move_used
    global dmg_dealt
    global choice
    global playername
    global rivalname
    global rival_move_used
    print("Starting battle....")
    wait(2000)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print('''
  ___          _     _     _            ___   _                  _     _ 
 | _ )  __ _  | |_  | |_  | |  ___     / __| | |_   __ _   _ _  | |_  | |
 | _ \ / _` | |  _| |  _| | | / -_)    \__ \ |  _| / _` | | '_| |  _| |_|
 |___/ \__,_|  \__|  \__| |_| \___|    |___/  \__| \__,_| |_|    \__| (_)
                                                                         ''')
    wait(2000)
    print("\n\n\nRival {} sent out {}.\n".format(rivalname, RivalPoke1.name))
    wait(2000)
    print("<{}> Go! {}!".format(playername, PlayerPoke1.name))
    wait(2000)


    while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("===================================================")
        print("HP [{}]                {}".format(getHealthBars(PlayerPoke1, RivalPoke1)[1], RivalPoke1.name))
        print("\n\n\n")
        print("HP [{}] {}/{}        {}".format(getHealthBars(PlayerPoke1, RivalPoke1)[0],addZeroes(PlayerPoke1.hp, 3), addZeroes(PlayerPoke1.Max_HP, 3), PlayerPoke1.name))
        print("===================================================")


        print("Select a move to use:")
        print("1. {}PP: {}".format(addWhitespace(PlayerPoke1.moves[0], 20), PlayerPoke1.PP[0]))
        print("2. {}PP: {}".format(addWhitespace(PlayerPoke1.moves[1], 20), PlayerPoke1.PP[1]))
        print("3. {}PP: {}".format(addWhitespace(PlayerPoke1.moves[2], 20), PlayerPoke1.PP[2]))
        print("4. {}PP: {}".format(addWhitespace(PlayerPoke1.moves[3], 20), PlayerPoke1.PP[3]))
        choice = askForLimitedNumber("Pick a number: ", 1, 4)
        if PlayerPoke1.moves[choice - 1] == "None":
            while True:
                print("\nThat's not a move, silly!")
                wait(1000)
                choice = askForLimitedNumber("Pick a number: ", 1, 4)
                if not(PlayerPoke1.moves[choice - 1] == "None"):
                    break
        if int(PlayerPoke1.PP[choice - 1]) == 0:
            while True:
                print("\n{} has no PP left for that move.".format(PlayerPoke1.name))
                wait(1000)
                choice = askForLimitedNumber("Pick a number: ", 1, 4)
                if not(int(PlayerPoke1.PP[choice - 1]) == 0):
                    break
        move_used = PlayerPoke1.moves[choice - 1]


        #This section determines the move used by the rival Pokemon. It currently only takes into account the amount of damage that would be dealt by each move, and makes a weighted random selection, with each move having a weight of its damage plus its PP, times the move's accuracy. This system needs to be improved upon in the future.
        rival_usable_moves = []
        try:
            score1 = (RivalPoke1.GetDamage(PlayerPoke1, RivalPoke1.moves[0]) * int(RivalPoke1.GetMove(move_used)[6])) + RivalPoke1.PP[0] * int(RivalPoke1.GetMove(move_used)[6])
        except:
            score1 = RivalPoke1.PP[0]
        try:
            score2 = (RivalPoke1.GetDamage(PlayerPoke1, RivalPoke1.moves[1]) * int(RivalPoke1.GetMove(move_used)[6])) + RivalPoke1.PP[1] * int(RivalPoke1.GetMove(move_used)[6])
        except:
            score2 = RivalPoke1.PP[1]
        try:
            score3 = (RivalPoke1.GetDamage(PlayerPoke1, RivalPoke1.moves[2]) * int(RivalPoke1.GetMove(move_used)[6])) + RivalPoke1.PP[2] * int(RivalPoke1.GetMove(move_used)[6])
        except:
            score3 = RivalPoke1.PP[2]
        try:
            score4 = (RivalPoke1.GetDamage(PlayerPoke1, RivalPoke1.moves[3]) * int(RivalPoke1.GetMove(move_used)[6])) + RivalPoke1.PP[3] * int(RivalPoke1.GetMove(move_used)[6])
        except:
            score4 = RivalPoke1.PP[3]



        for i in range(score1):
            rival_usable_moves.append(RivalPoke1.moves[0])
        for i in range(score2):
            rival_usable_moves.append(RivalPoke1.moves[1])
        for i in range(score3):
            rival_usable_moves.append(RivalPoke1.moves[2])
        for i in range(score4):
            rival_usable_moves.append(RivalPoke1.moves[3])

        rival_move_used = rival_usable_moves[random.randint(0,len(rival_usable_moves))]
        
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        if PlayerPoke1.SPD >= RivalPoke1.SPD:
            playerUseMove()
            wait(2000)
        else:
            rivalUseMove()
            wait(2000)



        if PlayerPoke1.hp < 1:
            print("{} fainted.".format(PlayerPoke1.name))
            wait(2000)
            print("You lost.")
            PlayerPoke1.hp = PlayerPoke1.Max_HP
            RivalPoke1.hp = PlayerPoke1.Max_HP
            PlayerPoke1.PP = [int(PlayerPoke1.GetMove(i)[4]) for i in PlayerPoke1.moves]
            RivalPoke1.PP = [int(RivalPoke1.GetMove(i)[4]) for i in RivalPoke1.moves]
            input("Type anything to continue: ")
            return
        elif RivalPoke1.hp < 1:
            print("Rival {} fainted!".format(RivalPoke1.name))
            wait(2000)
            print("You won!")
            PlayerPoke1.hp = PlayerPoke1.Max_HP
            RivalPoke1.hp = PlayerPoke1.Max_HP
            PlayerPoke1.PP = [int(PlayerPoke1.GetMove(i)[4]) for i in PlayerPoke1.moves]
            RivalPoke1.PP = [int(RivalPoke1.GetMove(i)[4]) for i in RivalPoke1.moves]
            input("Type anything to continue: ")
            return

        if PlayerPoke1.SPD >= RivalPoke1.SPD:
            rivalUseMove()
            wait(2000)
        else:
            playerUseMove()
            wait(2000)



        if PlayerPoke1.hp < 1:
            print("{} fainted.".format(PlayerPoke1.name))
            wait(2000)
            print("You lost.")
            PlayerPoke1.hp = PlayerPoke1.Max_HP
            RivalPoke1.hp = PlayerPoke1.Max_HP
            PlayerPoke1.PP = [int(PlayerPoke1.GetMove(i)[4]) for i in PlayerPoke1.moves]
            RivalPoke1.PP = [int(RivalPoke1.GetMove(i)[4]) for i in RivalPoke1.moves]
            input("Type anything to continue: ")
            return
        elif RivalPoke1.hp < 1:
            print("Rival {} fainted!".format(RivalPoke1.name))
            wait(2000)
            print("You won!")
            PlayerPoke1.hp = PlayerPoke1.Max_HP
            RivalPoke1.hp = PlayerPoke1.Max_HP
            PlayerPoke1.PP = [int(PlayerPoke1.GetMove(i)[4]) for i in PlayerPoke1.moves]
            RivalPoke1.PP = [int(RivalPoke1.GetMove(i)[4]) for i in RivalPoke1.moves]
            input("Type anything to continue: ")
            return

def mainMenu():
    global PlayerPoke1
    global RivalPoke1
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print('''
===============================================================
|  __  __          _            __  __                        |
| |  \/  |  __ _  (_)  _ _     |  \/  |  ___   _ _    _  _    |
| | |\/| | / _` | | | | ' \    | |\/| | / -_) | ' \  | || |   |
| |_|  |_| \__,_| |_| |_||_|   |_|  |_| \___| |_||_|  \_,_|   |
|                                                             |
===============================================================
 ''')
                                                          
    print("Welcome to the Pokémon Battle Simulator!")
    print("Please select an option below:\n")
    print("1. Load from save file")
    print("2. Create new Pokémon to battle")
    print("3. Battle with existing Pokémon")
    print("4. Manage saves")
    print("5. About")
    print("6. How to play")
    print("7. Quit")
    choice = askForLimitedNumber("\nEnter a number: ", 1, 7)


    if choice == 1:
        getInfoFromSave()
        mainMenu()
    elif choice == 2:
        makeNewPokemon()
        wait(2000)
        mainMenu()
    elif choice == 3:
        if PlayerPoke1 == None or RivalPoke1 == None:
            print("You haven't loaded a save file!")
            print("Load a save file or make new Pokémon before battling!")
            input("Type anything to continue: ")
            print("")
            mainMenu()
        else:
            battle()
            mainMenu()
    elif choice == 4:
        manageMenu()
    elif choice == 5:
        print('''
Hello there, DR4G0NW4RR10R here, and this is my Pokémon Battle simulator.
I made this project in Python 3, and I am improving it as time goes on, adding
more little features and things. Currently, this project had over 1200
lines of code!

This is not a perfect game, and there will be bugs. If you do find a bug or
two, please do let me know and I will do my best to patch it up.

If you would like a specific feature added, let me know and I'll see if I can
implement it.

Feedback link:
https://forms.gle/wdV6MFvbZbu76ow19

Special thanks to my beta testers for being amazing and trying this game:
- No one yet :*(
        ''')
        wait(5000)
        input("Type anything to continue ")
        mainMenu()
    elif choice == 6:
        print('''
Here are the basics of the game:

The Pokémon Battle Simulator is a simulator to simulate two Pokémon fighting
each other. You, the player, can specify almost all aspects of these Pokémon.
If you have an existing save file, it will have the information of the two
Pokémon that have been made. Included by default is a single save file to
serve as a preset battle, should you be interested.

Alternitavely, you can create two brand new Pokémon to battle with and pit
them up against each other! If you do this, you will be prompted to enter
information for these Pokémon.

Please note that currently Statuses, Abilities, and Pokémon Natures are
unimplemented, they cannnot be utilized in battle.
        ''')
        wait(5000)
        input("Type anything to continue ")
        mainMenu()
    elif choice == 7:
        print("Bye!")
        log("Program terminated")
        sys.exit(0)

def manageMenu():
    global PlayerPoke1
    global RivalPoke1
    global playername
    global rivalname
    global choice
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print('''
===============================================================================
|  __  __                                       ___                           |
| |  \/  |  __ _   _ _    __ _   __ _   ___    / __|  __ _  __ __  ___   ___  |
| | |\/| | / _` | | ' \  / _` | / _` | / -_)   \__ \ / _` | \ V / / -_) (_-<  |
| |_|  |_| \__,_| |_||_| \__,_| \__, | \___|   |___/ \__,_|  \_/  \___| /__/  |
|                               |___/                                         |
===============================================================================
    ''')
    print("Managing saves")
    print("Please select an option below:\n")
    print("1. Save current Pokémon to main save")
    print("2. Save current Pokémon to backup save")
    print("3. Create backup of main save")
    print("4. Override main save with backup save")
    print("5. Peek into a save")
    print("6. Back to main menu")
    choice = askForLimitedNumber("\nEnter a number: ", 1, 6)
    
    if choice == 1:
        if PlayerPoke1 == None or RivalPoke1 == None:
            print("Create some Pokémon first!")
            wait(2000)
            manageMenu()
        else:
            save_1 = playername
            save_2 = rivalname
            save_3 = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(PlayerPoke1.name, PlayerPoke1.pokemon, PlayerPoke1.level, PlayerPoke1.p_type[0], RivalPoke1.p_type[1], PlayerPoke1.moves[0], PlayerPoke1.moves[1], PlayerPoke1.moves[2], PlayerPoke1.moves[3], PlayerPoke1.HP_EV, PlayerPoke1.ATK_EV, PlayerPoke1.DEF_EV, PlayerPoke1.SPD_EV, PlayerPoke1.Sp_EV, PlayerPoke1.HP_IV, PlayerPoke1.ATK_IV, PlayerPoke1.DEF_IV, PlayerPoke1.SPD_IV, PlayerPoke1.Sp_IV, PlayerPoke1.hp)
            save_4 = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(RivalPoke1.name, RivalPoke1.pokemon, RivalPoke1.level, RivalPoke1.p_type[0], RivalPoke1.p_type[1], RivalPoke1.moves[0], RivalPoke1.moves[1], RivalPoke1.moves[2], RivalPoke1.moves[3], RivalPoke1.HP_EV, RivalPoke1.ATK_EV, RivalPoke1.DEF_EV, RivalPoke1.SPD_EV, RivalPoke1.Sp_EV, RivalPoke1.HP_IV, RivalPoke1.ATK_IV, RivalPoke1.DEF_IV, RivalPoke1.SPD_IV, RivalPoke1.Sp_IV, RivalPoke1.hp)
            
            savefile = open("Saves/save.txt", "w")
            savefile.write(save_1)
            savefile.write("\n")
            savefile.write(save_2)
            savefile.write("\n")
            savefile.write(save_3)
            savefile.write("\n")
            savefile.write(save_4)
            savefile.close()
            print("Save sucessfully updated!")
            wait(2000)
            manageMenu()
    elif choice == 2:
        if PlayerPoke1 == None or RivalPoke1 == None:
            print("Create some Pokémon first!")
            wait(2000)
            manageMenu()
        else:
            save_1 = playername
            save_2 = rivalname
            save_3 = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(PlayerPoke1.name, PlayerPoke1.pokemon, PlayerPoke1.level, PlayerPoke1.p_type[0], RivalPoke1.p_type[1], PlayerPoke1.moves[0], PlayerPoke1.moves[1], PlayerPoke1.moves[2], PlayerPoke1.moves[3], PlayerPoke1.HP_EV, PlayerPoke1.ATK_EV, PlayerPoke1.DEF_EV, PlayerPoke1.SPD_EV, PlayerPoke1.Sp_EV, PlayerPoke1.HP_IV, PlayerPoke1.ATK_IV, PlayerPoke1.DEF_IV, PlayerPoke1.SPD_IV, PlayerPoke1.Sp_IV, PlayerPoke1.hp)
            save_4 = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(RivalPoke1.name, RivalPoke1.pokemon, RivalPoke1.level, RivalPoke1.p_type[0], RivalPoke1.p_type[1], RivalPoke1.moves[0], RivalPoke1.moves[1], RivalPoke1.moves[2], RivalPoke1.moves[3], RivalPoke1.HP_EV, RivalPoke1.ATK_EV, RivalPoke1.DEF_EV, RivalPoke1.SPD_EV, RivalPoke1.Sp_EV, RivalPoke1.HP_IV, RivalPoke1.ATK_IV, RivalPoke1.DEF_IV, RivalPoke1.SPD_IV, RivalPoke1.Sp_IV, RivalPoke1.hp)
            
            print("Name the backup. Type CANCEL to cancel")
            print("WARNING! Entering the name of an existing backup will override it!")
            choice = input("Enter a name: ")
            if choice == "CANCEL":
                print("action cancelled.")
                wait(2000)
                manageMenu()
            
            savefile = open("Saves/{}.txt".format(choice), "w")
            savefile.write(save_1)
            savefile.write("\n")
            savefile.write(save_2)
            savefile.write("\n")
            savefile.write(save_3)
            savefile.write("\n")
            savefile.write(save_4)
            savefile.close()
            print("Sucessfully saved backup as \"{}.txt\" in the Saves folder.".format(choice))
            wait(4000)
            manageMenu()
    elif choice == 3:
        print("Name the backup. Type CANCEL to cancel")
        print("WARNING! Entering the name of an existing backup will override it!")
        choice = input("Enter a name: ")
        if choice == "CANCEL":
                print("action cancelled.")
                wait(2000)
                manageMenu()
                
        copyfile("Saves/save.txt", "Saves/{}.txt".format(choice))
        print("Sucessfully saved backup as \"{}.txt\" in the Saves folder.".format(choice))
        wait(4000)
        manageMenu()
    elif choice == 4:
        choice = input("Enter name of backup. Type CANCEL to cancel. ")
        if choice == "CANCEL":
                print("action cancelled.")
                wait(2000)
                manageMenu()
        try:
            copyfile("Saves/{}.txt".format(choice), "Saves/save.txt")
        except:
            print("That backup file does not exist.")
            wait(2000)
            manageMenu()
        print("Main save sucessfully overridden with {}.txt".format(choice))
        wait(2000)
        manageMenu()
    elif choice == 5:
        peekname = input("Enter a save name. Enter \"save\" to peek into the main save: ")
        skipExcept = False
        try:
            peek_file = open("Saves/{}.txt".format(peekname), "r")
            savedata = []

            for line in peek_file.readlines():
                otherlist.append(line.replace('\n', ''))
            for i in otherlist:
                savedata.append(i.split(','))

            print("\nPeeking into save....\n")
            playername = savedata[0][0]
            print("Player name: {}".format(playername))
            rivalname = savedata[1][0]
            print("Rival name: {}".format(rivalname))



            if savedata[2][4] == "None":
                PeekPlayerPoke1 = Pokemon(name=savedata[2][0], p_type=[savedata[2][3]], pokemon=savedata[2][1], level=int(savedata[2][2]), hp=int(savedata[2][19]))
            else:
                PeekPlayerPoke1 = Pokemon(name=savedata[2][0], p_type=[savedata[2][3], savedata[2][4]], pokemon=savedata[2][1], level=int(savedata[2][2]), hp=int(savedata[2][19]))

            PeekPlayerPoke1.HP_EV = int(savedata[2][9])
            PeekPlayerPoke1.ATK_EV = int(savedata[2][10])
            PeekPlayerPoke1.DEF_EV = int(savedata[2][11])
            PeekPlayerPoke1.SPD_EV = int(savedata[2][12])
            PeekPlayerPoke1.Sp_EV = int(savedata[2][13])
            PeekPlayerPoke1.HP_IV = int(savedata[2][14])
            PeekPlayerPoke1.ATK_IV = int(savedata[2][15])
            PeekPlayerPoke1.DEF_IV = int(savedata[2][16])
            PeekPlayerPoke1.SPD_IV = int(savedata[2][17])
            PeekPlayerPoke1.Sp_IV = int(savedata[2][18])
            PeekPlayerPoke1.UpdateStats()
            PeekPlayerPoke1.hp = int(savedata[2][19])
            PeekPlayerPoke1.moves = savedata[2][5:9]
            PeekPlayerPoke1.PP = [int(PeekPlayerPoke1.GetMove(i)[4]) for i in PeekPlayerPoke1.moves]

            print("{}'s Pokemon: {} the level {} {}.".format(playername, PeekPlayerPoke1.name, PeekPlayerPoke1.level, PeekPlayerPoke1.pokemon))


            if savedata[3][4] == "None":
                PeekRivalPoke1 = Pokemon(name=savedata[3][0], p_type=[savedata[3][3]], pokemon=savedata[3][1], level=int(savedata[3][2]), hp=int(savedata[3][19]))
            else:
                PeekRivalPoke1 = Pokemon(name=savedata[3][0], p_type=[savedata[3][3], savedata[3][4]], pokemon=savedata[3][1], level=int(savedata[3][2]), hp=int(savedata[3][19]))

            PeekRivalPoke1.HP_EV = int(savedata[3][9])
            PeekRivalPoke1.ATK_EV = int(savedata[3][10])
            PeekRivalPoke1.DEF_EV = int(savedata[3][11])
            PeekRivalPoke1.SPD_EV = int(savedata[3][12])
            PeekRivalPoke1.Sp_EV = int(savedata[3][13])
            PeekRivalPoke1.HP_IV = int(savedata[3][14])
            PeekRivalPoke1.ATK_IV = int(savedata[3][15])
            PeekRivalPoke1.DEF_IV = int(savedata[3][16])
            PeekRivalPoke1.SPD_IV = int(savedata[3][17])
            PeekRivalPoke1.Sp_IV = int(savedata[3][18])
            PeekRivalPoke1.UpdateStats()
            PeekRivalPoke1.hp = int(savedata[3][19])
            PeekRivalPoke1.moves = savedata[3][5:9]
            PeekRivalPoke1.PP = [int(PeekRivalPoke1.GetMove(i)[4]) for i in PeekRivalPoke1.moves]

            print("{}'s Pokemon: {} the level {} {}.".format(rivalname, PeekRivalPoke1.name, PeekRivalPoke1.level, PeekRivalPoke1.pokemon))
            log("\n\nSave file {} peeked at: {} vs rival {}.".format(peekname, PeekPlayerPoke1.name, PeekRivalPoke1.name))
            print("")
            input("Type anything to continue ")
            skipExcpet = True
            manageMenu()
        except:
            if not(skipExcept):
                if choice == 6:
                    sys.exit(0)
                print("Something went wrong. Make sure you typed in the name correctly, and that the save is formatted correctly.")
                wait(3000)
                manageMenu()
    elif choice == 6:
        mainMenu()

#=====================================================================================================================

log("\n\n\n\nProgram initiated ==========================================================================")
log("Please note the log currently only records battles.")


mainMenu()


log("Program terminated.")