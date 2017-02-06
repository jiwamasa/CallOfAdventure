# Create database
db = DAL("sqlite://storage.sqlite")

# Table containing quests to take
db.define_table('quests',
                Field('title'),
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
                Field('attack', 'integer', default=0),
                Field('defense', 'integer', default=0),
                Field('speed', 'integer', default=0),
                Field('cost', 'integer', readable=True),
                Field('category', 'integer', default=0), # index to equip_list
                Field('details', 'text'))

# Table containing equipment loadout sets (created by users)
db.define_table('loadouts',
                Field('name', unique=True),
                Field('creator', 'integer'), # user id
                Field('equip_list', 'list:integer')) # equip_item ids

# Table mapping equipment types to indeces (id) in equip_list
db.define_table('equip_types', Field('name'))

from gluon.tools import Auth
auth = Auth(db)
auth.settings.extra_fields['auth_user']= [
    Field('gold', 'integer', readable=True, writable=True),
    Field('cost_to_hire', 'integer', readable=True, writable=True),
    Field('inventory', 'list:integer', default=[]),
    Field('curr_loadout', 'integer', 0), # Currently equipped loadout
    Field('saved_loadouts', 'list:integer') # All saved loadouts
]
auth.define_tables(username=True)
