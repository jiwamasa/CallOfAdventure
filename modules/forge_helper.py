#calculates forged weapon stats as 4-tuple [type, atk, def, spd]
#rareore affects stat total
#booze affects randomness
#words of encouragement affect type and stat distribution

from gluon import *
from gluon.custom_import import track_changes
track_changes(True)

import random

NUM_EQUIP_TYPES = 6 #how many equip types there are

def calcStats(rareore, booze, words):
    print 'in:'
    print rareore
    print booze
    print words
    #get stat total based on rare ore and drunkness
    #at 0 booze, no change. at 100 booze, can go from 0 to 1.5 times
    rand_err = (float(random.randint(100-booze, 100+(booze/2))))/100
    print rand_err
    stat_total = (rareore**(1./3))*rand_err
    print stat_total
    #decide weapon type and stat distribution from words of encouragement
    item_type = 0
    atk_ratio = float(0)
    def_ratio = float(0)
    spd_ratio = float(0)
    for c in words:
        item_type += ord(c)
        if ord(c) < 65: #spaces, numbers, and punctuation
            spd_ratio += 1
            print 'spd'
        elif ord(c) < 97: #CAPITAL LETTERS FOR YELLING
            atk_ratio += 1
            print 'atk'
        else: #lower-case letters and everything else
            def_ratio += 1
            print 'def'
    print atk_ratio
    print def_ratio
    print spd_ratio
    item_type = (item_type % NUM_EQUIP_TYPES)+1
    speed = int((spd_ratio/float(len(words)))*stat_total) or -2
    attack = int((atk_ratio/float(len(words)))*stat_total) or -2
    defense = int((def_ratio/float(len(words)))*stat_total) or -2
    stats = [item_type,attack,defense,speed]
    print stats
    return(stats)
