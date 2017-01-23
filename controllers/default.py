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

#quest adding page (shouldn't be public in final build)
@auth.requires_login()
def addQuest():
    grid = SQLFORM.smartgrid(db.quests)
    return dict(grid=grid)

def user():
    return dict(form=auth())
