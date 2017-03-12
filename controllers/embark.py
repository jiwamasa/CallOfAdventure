#-----------------------------#
#      embark_controller      #
#-----------------------------#

#handles all the unity game interactions

#import control
from gluon.custom_import import track_changes
track_changes(True)

#python lib modules
import random
import datetime


#sends data to unity game
#should ONLY be accessible by unity game, redirect otherwise
def web2unity():
    session.connect(request) #get the session of the unity game
    curr_user = db.auth_user(session.auth.user.id)
    print curr_user.first_name

    if not session.curr_quest:
        return "error: no active quest"
    quest = db.quests(session.curr_quest)
    stats = quest.location+"%"+str(quest.difficulty)+"%"
    if session.party:
        if session.party[0] != session.auth.user.id:
            session.party.insert(0, session.auth.user.id)
    else:
        session.party = [session.auth.user.id]
    for hire_id in session.party:
        hire = db.auth_user(hire_id)
        attack = 0
        defense = 0
        speed = 0
        if hire.curr_loadout:
            for equip_id in hire.curr_loadout.equip_list:
                if equip_id:
                    equip_item = db.equip_items(equip_id)
                    attack += equip_item.attack
                    defense += equip_item.defense
                    speed += equip_item.speed
            stats += hire.first_name+" "+hire.last_name+"%"
            stats += str(attack)+"%"+str(defense)+"%"+str(speed)+"%"
    print stats
    return stats

#embark on quest
#page with embedded unity game
def questEmbark():
    #check if we still have this quest
    quest_id=request.args(0, cast=int)
    valid_quest=False
    if session.quest_list:
        for quest in session.quest_list:
            if hasattr(quest, 'id') and quest.id==quest_id:
                valid_quest=True
        if not valid_quest:
            session.flash='Invaild Quest'
            redirect(URL('default', 'index'))
    else:
        session.flash='Invaild Quest'
        redirect(URL('default','index'))
    quest = db.quests(request.args(0, cast=int)) or redirect(URL('index'))
    session.curr_quest = quest.id
    redirect(URL('web2unity'))
    return dict()
