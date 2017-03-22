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
    #print "testing"
    #return "Cave%2%Bob%99%99%99" #TESTING
    print "attempting to connect to session..."
    session.connect(request) #get the session of the unity game
    if not session:
        print "bad session"
        return "error: bad session"
    curr_user = db.auth_user(session.auth.user.id)
    print curr_user.first_name + " has connected"

    if not session.curr_quest:
        print "no quest"
        return "error: no active quest"
    quest = db.quests(session.curr_quest)
    print "got quest"
    stats = quest.location+"%"+str(quest.difficulty)+"%"
    user_list = [session.auth.user.id] #list of people on quest
    if session.party:
        for hire_id in session.party:
            user_list.append(hire_id)
    for hire_id in user_list:
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
            stats += hire.first_name+"%"
            stats += str(attack)+"%"+str(defense)+"%"+str(speed)+"%"
    stats = stats[:-1] #remove trailing '%'
    print stats
    return stats

#embark on quest
#page with embedded unity game
def questEmbark():
    #check if we still have this quest
    quest_id=request.args(0, cast=int) or redirect(URL('default', 'index'))
    valid_quest=False
    if session.quest_list:
        for quest in session.quest_list:
            if hasattr(quest, 'id') and quest.id==quest_id:
                valid_quest=True
    if not valid_quest:
        session.flash='Invaild Quest'
        redirect(URL('default','index'))
    session.curr_quest = quest_id
    session.questWin = 0 #default quest is lost
    return dict(quest_id=quest_id)

#tell server whether quest was won or lost
def questComplete():
    session.connect(request) #get the session of the unity game
    #if args == 1, then it's a win, otherwise, loss
    win=request.args(0, cast=int) or 0
    if win == 1:
        session.questWin = 1
        print "win!"
    else:
        session.questWin = 0
        print "lose!"
    return
