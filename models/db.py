db = DAL("sqlite://storage.sqlite")

# Table containing quests to take
db.define_table('quests',
                Field('title', unique=True),
                Field('quest_giver'),
                Field('reward'),
                Field('details', 'text'))


# Table containing adventurers for hire
# db.define_table('adventurers',
#                 Field('name', unique=True),
#                 Field('hit points', 'int'),
#                 Field('attack', 'int'),
#                 format = '%(name)s')

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
