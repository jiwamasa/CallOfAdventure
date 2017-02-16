#-----------------------------#
#      default_controller     #
#-----------------------------#


#import control
from gluon.custom_import import track_changes
track_changes(True)

#python lib modules
import random
import datetime

#custom moudles
import quest_helper


#home page
@auth.requires_login()
def index():
    return dict()


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
                session.quest_list.append(quests[rand_id])
                rand_amount=rand_amount-1
            else:
                rand_amount=-1
    return dict(questList=session.quest_list)
    
#details about a certain quest
@auth.requires_login()
def showQuest():
    quest = db.quests(request.args(0, cast=int)) or redirect(URL('index'))
    return dict(quest=quest)

#result of quest
@auth.requires_login()
def questResult():
    quest = db.quests(request.args(0, cast=int)) or redirect(URL('index'))
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

#all hires page
@auth.requires_login()
def hirePage():
    hireList = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
    disband = FORM('', INPUT(_name='disband', _type='submit',
                             _value='Disband Party'))
    if disband.process().accepted: #if disband button is clicked
        session.party = [] #empty party
        response.flash = 'Party disbanded'
    return dict(hireList=hireList, disband=disband)

#details about a certain person to hire them
@auth.requires_login()
def showHire():
    hire = db.auth_user(request.args(0, cast=int)) or redirect(URL('index'))
    cost = hire.cost_to_hire or 0
    current_gold = db.auth_user(auth.user.id).gold or 0
    form = FORM('', INPUT(_name='hire', _type='submit', _value='Hire'))
    if form.process().accepted: #when hire button is clicked...
        if session.party: #if party already started...
            if hire.id in session.party: #but already hired, alert user
                session.flash = 'Already hired ' + hire.first_name
                redirect(URL('hirePage'))
            else: #otherwise, add to party
                session.party.append(hire.id)
        else: #if party hasn't been started, create a new one
            session.party = [hire.id]
        if current_gold < cost: #if not enough money...
            session.party.remove(hire.id) #remove hire
            session.flash = 'Not enough gold to hire'
            redirect(URL('hirePage'))
        new_gold = current_gold - cost #deduct hiring cost 
        db.auth_user(auth.user.id).update_record(gold=new_gold) 
        new_gold = hire.gold + cost #add payment
        hire.update_record(gold=new_gold)
        session.flash = 'Successfully hired adventurer ' + hire.first_name
        redirect(URL('hirePage'))
    return dict(hire=hire, cost=cost, form=form)

#shop_vars
#adding shop page
@auth.requires_login()
def shop():
    #need a system to choose what items are available...
    #maybe do it based on time?
    if not session.shop_items:
        session.shop_items=[]
    if not session.last_shop_time:
        session.last_shop_time=datetime.timedelta
    
    if session.last_shop_time:
        print(session.last_shop_time)
    itemList = db(db.equip_items.id<15).select(db.equip_items.ALL, orderby=db.equip_items.cost)
    return dict(itemList=itemList)

@auth.requires_login()
def discussion():
    return dict()

@auth.requires_login()
def discussion_quests():
    form = SQLFORM(db.discussion_quests)
    if form.process().accepted:
        response.flash = 'Your comment was posted'
    comments = db().select(db.discussion_quests.ALL, orderby=db.discussion_quests.author)
    return dict(comments=comments, form=form)

@auth.requires_login()
def discussion_equipment():
    form = SQLFORM(db.discussion_equipment)
    if form.process().accepted:
        response.flash = 'Your comment was posted'
    comments = db().select(db.discussion_equipment.ALL, orderby=db.discussion_equipment.author)
    return dict(comments=comments, form=form)

@auth.requires_login()
def discussion_other():
    form = SQLFORM(db.discussion_other)
    if form.process().accepted:
        response.flash = 'Your comment was posted'
    comments = db().select(db.discussion_other.ALL, orderby=db.discussion_other.author)
    return dict(comments = comments, form = form)

#adding preview item to buy page
@auth.requires_login()
def showBuyItem():
    buyItem = db.equip_items(request.args(0, cast=int)) or redirect(URL('index'))
    cost = buyItem.cost or 0
    current_gold = db.auth_user(auth.user.id).gold or 0
    current_inv = db.auth_user(auth.user.id).inventory

    buyNow = FORM('', INPUT(_name='buyNow', _type='submit', _value='Buy'))
    goPrevious = FORM('', INPUT(_name='goPrevious', _type='submit', _value='Cancel'))
    if buyNow.process(formname='buy_now').accepted: #if buy button pressed
        if current_gold < cost: #insufficient funds
            session.flash = 'Not enough gold to buy the item'
            redirect(URL('shop'))
        else: #sufficient funds;
            new_gold = current_gold - cost #transact
            db.auth_user(auth.user.id).update_record(gold=new_gold)
            current_inv.append(int(buyItem.id)) #add bought item to inventory
            db.auth_user(auth.user.id).update_record(inventory=current_inv)
            session.flash = (buyItem.name) + " has been purchased!"
            redirect(URL('shop'))
    if goPrevious.process(formname='go_previous').accepted:
        redirect(URL('shop'))

    return dict(buyItem=buyItem, cost=cost, buyNow=buyNow, goPrevious=goPrevious)

#profile page
@auth.requires_login()
def profilePage():
    current_user = db.auth_user(auth.user.id)
    #free money button (debug)
    form = FORM('', INPUT(_name='free', _type='submit', _value='FREE GOLD'))
    if form.process().accepted:
        new_gold = current_user.gold + 1000
        current_user.update_record(gold=new_gold)
        
    if request.args(0): #equipping items to current loadout
        equipped = db.equip_items(request.args(0))
        if not current_user.curr_loadout: #if first loadout, make new loadout
            new_loadout = db.loadouts.insert()
            current_user.update_record(curr_loadout=new_loadout)
        new_equip_list = db.loadouts(current_user.curr_loadout).equip_list or [0]*10
        new_equip_list[equipped.category] = equipped
        db.loadouts(current_user.curr_loadout).update_record(equip_list=new_equip_list)
        session.flash = 'Equipped ' + equipped.name
        redirect(URL("profilePage"))
    return dict(form=form, current_user=current_user)

def user():
    if request.args(0) == 'profile':
        redirect(URL('profilePage'))
    return dict(form=auth())
