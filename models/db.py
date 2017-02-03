# Create database
db = DAL("sqlite://storage.sqlite")

# Table containing quests to take
db.define_table('quests',
                Field('title', unique=True),
                Field('quest_giver'),
                Field('gold', 'integer'),
                Field('prestige', 'integer'),
                Field('difficulty', 'integer'),
                Field('location'),
                Field('loot_items', 'list:integer', default=[]),
                Field('details', 'text'))

# Table containing all items
db.define_table('equip_items',
                Field('name', unique=True),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('speed', 'integer'),
                Field('cost', 'integer', readable=True),
                Field('details', 'text'))

from gluon.tools import Auth
auth = Auth(db)
auth.settings.extra_fields['auth_user']= [
    Field('gold', 'integer', readable=True, writable=True),
    Field('cost_to_hire', 'integer', readable=True, writable=True),
    Field('inventory', 'list:integer', default=[])]
auth.define_tables(username=True)
