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
    session.connect(request) #get the session of the unity game
    curr_user = db.auth_user(session.auth.user.id)
    print curr_user.first_name
    stats = ""
    stats += curr_user.first_name + "%" + curr_user.last_name + "%"
    return stats

#page with embedded unity game
def questBattle():
    return dict()
