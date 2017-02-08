#default controller

#home page
@auth.requires_login()
def index():
    return dict()

#all quests page
@auth.requires_login()
def questsPage():
    questList = db().select(db.quests.ALL, orderby=db.quests.title)
    return dict(questList=questList)

#details about a certain quest
@auth.requires_login()
def showQuest():
    quest = db.quests(request.args(0, cast=int)) or redirect(URL('index'))
    db.auth_user(auth.user.id).update_record(curr_session_id=request.cookies["session_id_callofadventure"].value)
    return dict(quest=quest)

#result of quest
@auth.requires_login()
def questResult():
    quest = db.quests(request.args(0, cast=int)) or redirect(URL('index'))
    if session.party:
        party_strength=len(session.party)+1
    else:
        party_strength=1
    if float(party_strength)>=float(quest.difficulty):
        result_msg='was a success!'
        success = 1
        new_gold = quest.gold + db.auth_user(auth.user.id).gold
        db.auth_user(auth.user.id).update_record(gold=new_gold)
        user_items=db.auth_user(auth.user.id).inventory or []
        for item in quest.loot_items:
            user_items.append(item)
        db.auth_user(auth.user.id).update_record(inventory=user_items)
        response.flash = 'Success!'
    else:
        result_msg='was a failure...'
        success = 0
    return dict(quest=quest, result_msg=result_msg, success=success)

#quest adding page (shouldn't be public in final build)
@auth.requires_login()
def addQuest():
    grid = SQLFORM.smartgrid(db.quests)
    return dict(grid=grid)

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

#adding item page (shouldn't be public in final build)
@auth.requires_login()
def addItem():
    grid = SQLFORM.smartgrid(db.equip_items)
    return dict(grid=grid)



#adding shop page
@auth.requires_login()
def shop():
    itemList = db().select(db.equip_items.ALL, orderby=db.equip_items.cost)
    return dict(itemList=itemList)

#adding preview item to buy page
@auth.requires_login()
def showBuyItem():
    buyItem = db.equip_items(request.args(0, cast=int)) or redirect(URL('index'))
    cost = buyItem.cost or 0
    current_gold = db.auth_user(auth.user.id).gold or 0

    buyNow = FORM('', INPUT(_name='buyNow', _type='submit', _value='Buy'))
    goPrevious = FORM('', INPUT(_name='goPrevious', _type='submit', _value='Cancel'))
    if buyNow.process(formname='buy_now').accepted: #if buy button pressed
        if current_gold < cost: #transact
            session.flash = 'Not enough gold to buy the item'
            redirect(URL('shop'))
        else:
            new_gold = current_gold - cost
            db.auth_user(auth.user.id).update_record(gold=new_gold)
            session.flash = buyItem.name + " has been purchased!"
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
            new_loadout = db.loadouts.insert(creator=current_user.id)
            current_user.update_record(curr_loadout=new_loadout)
        new_equip_list = db.loadouts(current_user.curr_loadout).equip_list or [0]*10
        new_equip_list[equipped.category] = equipped
        db.loadouts(current_user.curr_loadout).update_record(equip_list=new_equip_list)
        session.flash = 'Equipped ' + equipped.name
        redirect(URL("profilePage"))
    return dict(form=form, current_user=current_user)

def unityTest():
    filename = 'applications/callofadventure/static/battle_stats/' + str(auth.user.id)
    stat_file = open(filename,'w')
    stat_file.write('hello file!\nstats go here.\n')
    return dict()

#depricated test method, use unitywrtest2 instead
def unitywrtest():
    return dict()

def unitywrtest2():
    #request_session_id = request.cookies["session_id_callofadventure"].value
    #questing_user = db(db.auth_user.curr_session_id == request_session_id).select().first()
    #quest_session = db(db.web2py_session_CallOfAdventure.unique_key == request_session_id[2:]).select().first()
    session.connect(request)
    print session.auth.user.first_name
    stats = ""
    stats += session.auth.user.first_name
    for party_id in session.party:
        stats+=db.auth_user(party_id).first_name
    #if not questing_user:
    #    stats = 'error, no matching user'
    #else:
        #PUT STATS ENCODED IN STRING HERE
        #WILL BE SENT TO UNITY TO BE PARSED
    #    stats = 'NAME:'+questing_user.first_name
    return stats


def status():
    return dict(session=session,request=request,response=response,auser=auth.user);

def user():
    if request.args(0) == 'profile':
        redirect(URL('profilePage'))
    return dict(form=auth())
