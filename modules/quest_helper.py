#quest_helper file

from gluon import *

from gluon.custom_import import track_changes
track_changes(True)

def monster_strength(diff):
    hp=diff*2
    atk=diff*2
    defense=diff*2
    return([hp,atk,defense])
    
def player_strength(db, auth_user):
    strength=0
    if auth_user.curr_loadout:
        for item in auth_user.curr_loadout.equip_list:
            if item:
                stats = item.attack+item.defense+item.speed
                strength=strength+stats
    return strength
    
def test():
    print(1)
    return 1
    
def test2(db):
    temp = db.auth_user(1)
    print(temp)
    return 0