# Create database
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

# Table containing all items
db.define_table('equip_items',
                Field('name', unique=True),
                Field('attack'),
                Field('defense'),
                Field('speed'),
                Field('cost'),
                Field('details', 'text'))

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
