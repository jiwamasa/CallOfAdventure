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
    form = FORM('', INPUT(_name='hire', _type='submit', _value='Hire'))
    if form.process().accepted: #when hire button is clicked
        #ADD CODE TO CHECK IF ENOUGH GOLD, THEN SUBTRACT
        if session.party: #if party already started...
            if hire.id in session.party: #but already hired, alert user
                session.flash = 'Already hired ' + hire.first_name
                redirect(URL('hirePage'))
            else: #otherwise, add to party
                session.party.append(hire.id)
        else: #if party hasn't been started, create a new one
            session.party = [hire.id]
        session.flash = 'Successfully hired adventurer ' + hire.first_name
        redirect(URL('hirePage'))
    return dict(hire=hire, form=form)
    
def user():
    return dict(form=auth())
