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
                Field('reward'),
                Field('loot_items', 'list:integer', default=[]),
                Field('details', 'text'))

# Table containing all items
db.define_table('equip_items',
                Field('name', unique=True),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('speed', 'integer'),
                Field('cost', 'integer', readable=True),
                Field('type'),
                Field('details', 'text'))

db.equip_items.type.requires=IS_IN_SET('hand', 'head', 'chest', 'legs');

# Table containing equipment loadout sets (created by users)
db.define_table('loadouts',
                Field('name'),
                Field('creator', 'integer'), # User id
                Field('lhand_equip', 'integer'), # equip_item id
                Field('rhand_equip', 'integer'),
                Field('head_equip', 'integer'),
                Field('chest_equip', 'integer'),
                Field('legs_equip', 'integer'))

from gluon.tools import Auth
auth = Auth(db)
auth.settings.extra_fields['auth_user']= [
    Field('gold', 'integer', readable=True, writable=True),
    Field('cost_to_hire', 'integer', readable=True, writable=True),
    Field('inventory', 'list:integer', default=[]),
    Field('curr_loadout', 'integer'), # Currently equipped loadout
    Field('saved_loadouts', 'list:integer') # All saved loadouts
]
auth.define_tables(username=True)
