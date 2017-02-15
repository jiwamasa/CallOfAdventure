# Create database
db = DAL("sqlite://storage.sqlite")

# Table mapping equipment types to indeces (id) in equip_list
db.define_table('equip_types', Field('name'))

# Table containing all items
db.define_table('equip_items',
                Field('name', unique=True),
                Field('attack', 'integer', default=0),
                Field('defense', 'integer', default=0),
                Field('speed', 'integer', default=0),
                Field('cost', 'integer', readable=True),
                Field('category', 'reference equip_types', default=0),
                Field('details', 'text'))

# Table containing equipment loadout sets (created by users)
db.define_table('loadouts',
                Field('name', unique=True),
                Field('equip_list', 'list:reference equip_items'))

# User database
from gluon.tools import Auth
auth = Auth(db)
auth.settings.extra_fields['auth_user']= [
    Field('gold', 'integer', readable=True, writable=True),
    Field('rare_ore', 'integer', readable=True, writable=True),
    Field('cost_to_hire', 'integer', readable=True, writable=True),
    Field('inventory', 'list:reference equip_items', default=[], readable=True, writable=True),
    Field('curr_loadout', 'reference loadouts', 0),
    Field('saved_loadouts', 'list:reference loadouts')]
auth.define_tables(username=True)

# Table containing quests to take
db.define_table('quests',
                Field('title'),
                Field('quest_giver'),
                Field('gold', 'integer'),
                Field('prestige', 'integer'),
                Field('difficulty', 'integer'),
                Field('location'),
                Field('loot_items', 'list:reference equip_items', default=[]),
                Field('details', 'text'))

# Discussion pages
db.define_table('discussion_quests',
                Field('author'),
                Field('body', 'text'))
db.define_table('discussion_equipment',
                Field('author'),
                Field('body', 'text'))
db.define_table('discussion_other',
                Field('author'),
                Field('body', 'text'))
