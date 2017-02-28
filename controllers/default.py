#-----------------------------#
#      default_controller     #
#-----------------------------#


#import control
from gluon.custom_import import track_changes
track_changes(True)

#python lib modules
import random
import datetime

#custom modules

#home page
@auth.requires_login()
def index():
    if not session.last_shop_time:
        session.last_shop_time=datetime.datetime.now()
    rows = db(db.image).select()
    first_row = rows[0]
    second_row = rows[1]
    return dict(first_row = first_row, second_row = second_row)

def download():
    return response.download(request, db)

#Middle point for shop and quests
#items with stat total less the this go into shop
#quest loot is higher than this
ITEM_MID = 20
#base rate of 25%, +5% per difficulty level
RARE_ITEM_RATE = 0.25
RARE_ITEM_RATE_ADD = 0.05

#all hires page
@auth.requires_login()
def hirePage():
    hireList = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
    disband = FORM('', INPUT(_name='disband', _type='submit',
                             _value='Disband Party'))
    if disband.process().accepted: #if disband button is clicked
        session.party = [] #empty party
        response.flash = 'Party disbanded'
    return dict(hireList=hireList, disband=disband)

#details about a certain person to hire them
@auth.requires_login()
def showHire():
    hire = db.auth_user(request.args(0, cast=int)) or redirect(URL('index'))
    cost = hire.cost_to_hire or 0
    current_gold = db.auth_user(auth.user.id).gold or 0
    form = FORM('', INPUT(_name='hire', _type='submit', _value='Hire'))
    if form.process().accepted: #when hire button is clicked...
        if session.party: #if party already started...
            if hire.id in session.party: #but already hired, alert user
                session.flash = 'Already hired ' + hire.first_name
                redirect(URL('hirePage'))
            else: #otherwise, add to party
                session.party.append(hire.id)
        else: #if party hasn't been started, create a new one
            session.party = [hire.id]
        if current_gold < cost: #if not enough money...
            session.party.remove(hire.id) #remove hire
            session.flash = 'Not enough gold to hire'
            redirect(URL('hirePage'))
        new_gold = current_gold - cost #deduct hiring cost 
        db.auth_user(auth.user.id).update_record(gold=new_gold) 
        new_gold = hire.gold + cost #add payment
        hire.update_record(gold=new_gold)
        session.flash = 'Successfully hired adventurer ' + hire.first_name
        redirect(URL('hirePage'))
    return dict(hire=hire, cost=cost, form=form)

#shop page
@auth.requires_login()
def shop():
    update=0
    if not session.shop_items:
        session.shop_items=[]
    if not session.last_shop_time:
        session.last_shop_time=datetime.datetime.now()
    
    if session.last_shop_time:
        time=datetime.datetime.now()
        delta=time-session.last_shop_time
        #update every 30 seconds right now
        if(delta.seconds>30 or delta.days>0):
            session.last_shop_time=datetime.datetime.now()
            session.shop_items=[]
            #session.flash='new items!' out of sync?
            update=1
            #print('update')
            #items=db(db.equip_items.id<15).select(db.equip_items.ALL)
            #select based on stat total
            items=db((db.equip_items.attack+db.equip_items.defense+db.equip_items.speed)<=ITEM_MID).select(db.equip_items.ALL)
            #give them 3 items
            items_needed=random.randint(4,7)
            while items_needed>0:
                rand_id=random.randint(0,len(items)-1)
                session.shop_items.append(items[rand_id])
                items_needed=items_needed-1  
        #print(str(delta))
    #itemList = db(db.equip_items.id<15).select(db.equip_items.ALL, orderby=db.equip_items.cost)
    return dict(itemList=session.shop_items, update=update)

@auth.requires_login()
def discussion():
    return dict()

@auth.requires_login()
def discussion_page():
    db.posts.category.default=request.args(0)
    db.posts.author.default=auth.user
    form = SQLFORM(db.posts)
    if form.process().accepted:
       response.flash = 'Comment posted!!'
    elif form.errors:
       response.flash = 'form has errors'
    #else:
       #response.flash = 'please fill out the form'
       
    posts=db(db.posts.category==request.args(0)).select(db.posts.ALL, orderby=~db.posts.post_date)
    return dict(posts=posts, form=form)

#adding preview item to buy page
@auth.requires_login()
def showBuyItem():
    buyItem = db.equip_items(request.args(0, cast=int)) or redirect(URL('index'))
    cost = buyItem.cost or 0
    current_gold = db.auth_user(auth.user.id).gold or 0
    current_inv = db.auth_user(auth.user.id).inventory

    buyNow = FORM('', INPUT(_name='buyNow', _type='submit', _value='Buy'))
    goPrevious = FORM('', INPUT(_name='goPrevious', _type='submit', _value='Cancel'))
    if buyNow.process(formname='buy_now').accepted: #if buy button pressed
        if current_gold < cost: #insufficient funds
            session.flash = 'Not enough gold to buy the item'
            redirect(URL('shop'))
        else: #sufficient funds;
            new_gold = current_gold - cost #transact
            db.auth_user(auth.user.id).update_record(gold=new_gold)
            current_inv.append(int(buyItem.id)) #add bought item to inventory
            db.auth_user(auth.user.id).update_record(inventory=current_inv)
            session.flash = (buyItem.name) + " has been purchased!"
            session.shop_items.remove(db.equip_items(buyItem.id))
            redirect(URL('shop'))
    if goPrevious.process(formname='go_previous').accepted:
        redirect(URL('shop'))

    return dict(buyItem=buyItem, cost=cost, buyNow=buyNow, goPrevious=goPrevious)

#profile page
@auth.requires_login()
def profilePage():
    current_user = db.auth_user(auth.user.id)
    #free money button (debug)
    form = FORM('', INPUT(_name='free', _type='submit', _value='FREE STUFF'))
    if form.process().accepted:
        new_gold = current_user.gold + 1000
        new_rare_ore = current_user.rare_ore + 100
        current_user.update_record(gold=new_gold)
        current_user.update_record(rare_ore=new_rare_ore)
        
    if request.args(0) == 'equip': #equipping items to current loadout
        equipped = db.equip_items(request.args(1))
        if not current_user.curr_loadout: #if first loadout, make new loadout
            new_loadout = db.loadouts.insert()
            current_user.update_record(curr_loadout=new_loadout)
        new_equip_list = db.loadouts(current_user.curr_loadout).equip_list or [0]*10
        new_equip_list[equipped.category] = equipped
        db.loadouts(current_user.curr_loadout).update_record(equip_list=new_equip_list)
        session.flash = 'Equipped ' + equipped.name
        redirect(URL("profilePage"))

    if request.args(0) == 'unequip': #unequipping items from current loadout
        unequipped = db.equip_items(request.args(1))
        new_equip_list = db.loadouts(current_user.curr_loadout).equip_list 
        new_equip_list[unequipped.category] = 0
        db.loadouts(current_user.curr_loadout).update_record(equip_list=new_equip_list)
        session.flash = 'Unequipped ' + unequipped.name
        redirect(URL("profilePage"))

    return dict(form=form, current_user=current_user)

def user():
    if request.args(0) == 'profile':
        redirect(URL('profilePage'))
    return dict(form=auth())
