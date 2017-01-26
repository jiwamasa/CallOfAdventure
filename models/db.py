db = DAL("sqlite://storage.sqlite")

# Table containing quests to take
db.define_table('quests',
                Field('title', unique=True),
                Field('quest_giver'),
                Field('gold'),
                Field('prestige'),
                Field('difficulty'),
                Field('location'),
                Field('reward'),
                Field('details', 'text'))

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
