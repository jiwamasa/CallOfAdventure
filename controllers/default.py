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
        new_gold = quest.gold + db.auth_user(auth.user.id).gold
        db.auth_user(auth.user.id).update_record(gold=new_gold)
    else:
        result_msg='was a failure...'
    return dict(quest=quest, result_msg=result_msg)

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
        new_gold = current_gold - cost
        db.auth_user(auth.user.id).update_record(gold=new_gold) #deduct hiring cost
        session.flash = 'Successfully hired adventurer ' + hire.first_name
        redirect(URL('hirePage'))
    return dict(hire=hire, cost=cost, form=form)

#adding item page (shouldn't be public in final build)
@auth.requires_login()
def addItem():
    grid = SQLFORM.smartgrid(db.equip_items)
    return dict(grid=grid)

#profile page
def profilePage():
    #free money button (debug)
    form = FORM('', INPUT(_name='free', _type='submit', _value='FREE GOLD'))
    if form.process().accepted:
        new_gold = db.auth_user(auth.user.id).gold + 1000
        db.auth_user(auth.user.id).update_record(gold=new_gold)
       
    return dict(form=form)

def user():
    if request.args(0) == 'profile':
        redirect(URL('profilePage'))
    return dict(form=auth())
