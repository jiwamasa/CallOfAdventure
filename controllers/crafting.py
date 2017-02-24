#controller for crafting items

#import control
from gluon.custom_import import track_changes
track_changes(True)

#custom moudles
import forge_helper


#forge equip items with rare ore
def forge():
    current_user = db.auth_user(auth.user.id)
    form = FORM('Rare Ore: ', INPUT(_name='rareore', _type='text', requires=IS_INT_IN_RANGE(1, current_user.rare_ore+1, error_message='Enter valid amount of Rare Ore')), BR(),
                'Booze: ', INPUT(_name='booze', _type='range'), BR(),
                'Words of Encouragement: ', INPUT(_name='words', _type='text', requires=IS_NOT_EMPTY(error_message='Let him know you care!')),
                BR(), INPUT(_type='submit', _value='FORGE!'))
    if form.accepts(request, session):
        #CHECK NAME FOR DUPLICATE (in form?)
        booze = int(form.vars.booze)
        rareore = int(form.vars.rareore)
        new_rare_ore = current_user.rare_ore - rareore
        current_user.update_record(rare_ore=new_rare_ore)
        stats = forge_helper.calcStats(rareore,booze,form.vars.words)
        forgeItem = db.equip_items.insert(name="Something",
                                          attack=stats[1],
                                          defense=stats[2],
                                          speed=stats[3],
                                          cost=100,
                                          category=stats[0],
                                          details="It's an item")
        current_inv = current_user.inventory
        current_inv.append(forgeItem)
        current_user.update_record(inventory=current_inv)
        redirect(URL('forgeResults', args=forgeItem))
    return dict(form=form)

#results of forging
def forgeResults():
    form = SQLFORM(db.equip_items, record=request.args(0), fields=['name','details'], showid=False)
    if form.process().accepted:
        redirect(URL('default', 'index'))
    return dict(forge_id=request.args(0),form=form)
