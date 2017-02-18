#controller for quest related actions

#import control
from gluon.custom_import import track_changes
track_changes(True)

#python lib modules
import random
import datetime

#custom moudles
import quest_helper


#---Necessary for Quest Generation---#
QUEST_MIN = 5
QUEST_MAX = 9
QUEST_ADD_MAX = 5
QUEST_ADD_MIN = 2

#all quests page
@auth.requires_login()
def questsPage():
    print(quest_helper.monster_strength(2))
    if not session.quest_list:
        session.quest_list=[]
    quest_count = len(session.quest_list)
    # over the limit?
    if quest_count>=QUEST_MAX:
        rand_remove=random.randint(0,len(session.quest_list)-1)
        session.quest_list.pop(rand_remove)
    # low on quests, add more
    elif quest_count <= QUEST_MIN:
        #calculate user strength here
        min_lvl = 0
        max_lvl = 100000
        quests = db(((db.quests.difficulty>=min_lvl) and (db.quests.difficulty<=max_lvl))).select(db.quests.ALL, orderby=db.quests.difficulty)
        rand_amount = random.randint(QUEST_ADD_MIN,QUEST_ADD_MAX)
        while rand_amount>0:
            if len(quests)>=1:
                rand_id = random.randint(0,len(quests)-1)
                if quests[rand_id].quest_giver.id != auth.user.id:
                    session.quest_list.append(quests[rand_id])
                rand_amount=rand_amount-1
            else:
                rand_amount=-1
    return dict(questList=session.quest_list)
    
#details about a certain quest
@auth.requires_login()
def showQuest():
    quest = db.quests(request.args(0, cast=int)) or redirect(URL('default', 'index'))
    return dict(quest=quest)

#result of quest
@auth.requires_login()
def questResult():
    quest = db.quests(request.args(0, cast=int)) or redirect(URL('default', 'index'))
    current_user = db.auth_user(auth.user.id)
    #calculate user power
    #hp, atk, def
    party_strength=[5.0,5.0,5.0]
    
    #calculate user's item power
    if current_user.curr_loadout > 0:
        loadout=db.loadouts(current_user.curr_loadout).equip_list
        for item_id in loadout:
            if item_id>0:
                item=db.equip_items(item_id)
                party_strength[1]=party_strength[1]+item.attack
                party_strength[2]=party_strength[2]+item.defense
                
    #calculate party power
    if session.party:
        for i in range(0,len(session.party)):
            #add up stats for each member, dummy for now
            party_strength=[sum(x) for x in zip(party_strength, [5.0,5.0,5.0])]
            
    monster_strength=[3.0*quest.difficulty,3.0*quest.difficulty,3.0*quest.difficulty]
     
    #main 'battle logic' take turns killing each other
    #loser is who reaches 0 health first
    while party_strength[0]>0.0 and monster_strength[0]>0.0:
        monster_strength[0]-=party_strength[1]
        party_strength[0]-=monster_strength[1]*(1-((1/100)*party_strength[2]))

    found_items=[]
    if party_strength[0]>=0.0:
        success = 1
        result_msg = 'was a success!'
        response.flash = 'Success!'
        new_gold = quest.gold + current_user.gold
        current_user.update_record(gold=new_gold)
        user_items=current_user.inventory
        
        # 50% chance to drop any one item, hardcoded right now
        for item in quest.loot_items:
            if random.random()>0.5:
                user_items.append(item)
                found_items.append(item)
        current_user.update_record(inventory=user_items)
        #give rare ore to user who posted quest
        new_rare_ore = 10*quest.difficulty + quest.quest_giver.rare_ore
        quest.quest_giver.update_record(rare_ore=new_rare_ore)
        
        if session.quest_list:
            session.quest_list.remove(quest)
    else:
        success = 0
        result_msg = 'was a failure...'      
    return dict(quest=quest, result_msg=result_msg, success=success, party_strength=party_strength, found_items=found_items)

#quest adding page
@auth.requires_login()
def addQuest():
    curr_user = db.auth_user(auth.user.id)
    db.quests.gold.requires=IS_INT_IN_RANGE(0,curr_user.gold,error_message='Not enough gold')
    form = SQLFORM(db.quests)
    if form.process().accepted:
        new_gold = curr_user.gold - form.vars.gold
        curr_user.update_record(gold=new_gold)
        db.quests(form.vars.id).update_record(quest_giver=curr_user)
        db.quests(form.vars.id).update_record(prestige=form.vars.difficulty)
        #RANDOMIZE LOOT ITEMS BASED ON DIFFCULTY
    return dict(form=form)
