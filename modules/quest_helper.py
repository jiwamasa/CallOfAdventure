#quest_helper file

from gluon import *

from gluon.custom_import import track_changes
track_changes(True)

def monster_strength(diff):
    hp=diff*2
    atk=diff*2
    defense=diff*2
    return([hp,atk,defense])