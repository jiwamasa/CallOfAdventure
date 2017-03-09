# Create database
db = DAL("sqlite://storage.sqlite")

# Table mapping equipment types to indeces (id) in equip_list
db.define_table('equip_types', Field('name'))

# Table containing all items
db.define_table('equip_items',
                Field('name'),
                Field('attack', 'integer', default=0),
                Field('defense', 'integer', default=0),
                Field('speed', 'integer', default=0),
                Field('cost', 'integer', default=0),
                Field('category', 'reference equip_types', default=0),
                Field('details', 'text'))

# Table defining all items that can be sold in shop
db.define_table('for_sale',
                Field('item', 'reference equip_items'),
                Field('rarity', 'integer'))

db.equip_items.name.requires=IS_LENGTH(maxsize=30, error_message="Name must be 30 characters or fewer")
db.equip_items.name.requires=IS_MATCH('^[a-zA-Z0-9\\-\\s]+$', error_message="Name can only contain letters, numbers, and spaces")
db.equip_items.details.requires=IS_LENGTH(maxsize=300, error_message="Description must be 300 characters or fewer")

# Table containing equipment loadout sets (created by users)
db.define_table('loadouts',
                Field('name'),
                Field('equip_list', 'list:reference equip_items', default=[0]*10))

# User database
from gluon.tools import Auth
auth = Auth(db)
auth.settings.extra_fields['auth_user']= [
    Field('gold', 'integer', default=500, readable=False, writable=False),
    Field('rare_ore', 'integer', default=0, readable=False, writable=False),
    Field('cost_to_hire', 'integer', default=10, readable=True, writable=True),
    Field('inventory', 'list:reference equip_items', default=[], readable=False, writable=False),
    Field('curr_loadout', 'reference loadouts', default=db.loadouts.insert(), writable=False),
    Field('saved_loadouts', 'list:reference loadouts', writable=False)]
auth.define_tables(username=True)

db.auth_user.cost_to_hire.requires=IS_INT_IN_RANGE(minimum=10, maximum=100000,
                                                   error_message="Invalid cost")

# Table containing quests to take
db.define_table('quests',
                Field('title', required=True, requires=IS_NOT_EMPTY()),
                Field('quest_giver', 'reference auth_user', readable=False, writable=False),
                Field('gold', 'integer', readable=True, writable=True, default=0),
                Field('prestige', 'integer', readable=False, writable=False),
                Field('difficulty', 'integer'),
                Field('location'),
                Field('loot_items', 'list:reference equip_items', default=[], readable=False, writable=False),
                Field('details', 'text'))

db.quests.difficulty.requires=IS_IN_SET(range(1,6))
db.quests.location.requires=IS_IN_SET(['Forest','Cave','Dungeon'])

# Discussion pages
import datetime

db.define_table('posts',
                Field('author', 'reference auth_user', readable=False, writable=False),
                Field('title', required=True, requires=IS_NOT_EMPTY()),
                Field('body', 'text', required=True, requires=IS_NOT_EMPTY()),
                Field('category', 'string', requires=IS_IN_SET(['Quests','Equipment','Other'],zero=T('choose one'),
                                                                                        error_message='choose a category')),
                Field('post_date', 'datetime', readable=True, writable=False, default=datetime.datetime.now()))

#Images for logo
db.define_table('image',
                Field('title', unique=True),
                Field('file', 'upload'),
                format = '%(title)s')
