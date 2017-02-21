#-----------------------------#
#      battle_controller      #
#-----------------------------#

#handles all the quest battle/unity game interactions

#import control
from gluon.custom_import import track_changes
track_changes(True)

#python lib modules
import random
import datetime


#sends data to unity game
#should ONLY be accessible by unity game, redirect otherwise
def web2unity():
    #CHECK IF UNITY (user_agent attr?) REDIRECT OTHERWISE
    #JUST CHECK IF SESSION HAS AN ACTIVE QUEST IN IT
    session.connect(request) #get the session of the unity game
    curr_user = db.auth_user(session.auth.user.id)
    print curr_user.first_name
    attack = 0
    defense = 0
    speed = 0
    if curr_user.curr_loadout:
        for equip_id in curr_user.curr_loadout.equip_list:
            if equip_id:
                equip_item = db.equip_items(equip_id)
                attack += equip_item.attack
                defense += equip_item.defense
                speed += equip_item.speed
    stats = "forest%" #hardcoded location for now
    stats += curr_user.first_name+"%"+curr_user.last_name+"%"
    stats += str(attack)+"%"+str(defense)+"%"+str(speed)+"%"
    return stats

#page with embedded unity game
def questBattle():
    return dict()
