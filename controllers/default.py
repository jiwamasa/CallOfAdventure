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
    #rows = db(db.image).select()
    #first_row = rows[0]
    #second_row = rows[1]
    return dict()

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
            #inject generic items into for_sale table
            weak_items = db(db.equip_items.id < 15).select(db.equip_items.ALL,
                                                           orderby='<random>',
                                                           limitby=(0,3))
            for item in weak_items:
                db.for_sale.insert(item=item)
            #add items to user's shop
            update=1
            session.last_shop_time=datetime.datetime.now()
            if len(session.shop_items) > 10: #remove surplus
                while len(session.shop_items) > 5:
                    session.shop_items.pop(random.randint(0,len(session.shop_items)-1))
            items=db().select(db.for_sale.ALL,
                              orderby='<random>',
                              limitby=(0,4+random.randint(0,3)))
            for sale_item in items:
                if not sale_item.item in session.shop_items:
                    session.shop_items.append(sale_item.item)
            response.flash='New items!'
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

#preview item to buy page
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
            session.flash = 'You can\'t afford this! Get out!'
            redirect(URL('shop'))
        else: #sufficient funds;
            new_gold = current_gold - cost #transact
            db.auth_user(auth.user.id).update_record(gold=new_gold)
            current_inv.append(int(buyItem.id)) #add bought item to inventory
            db.auth_user(auth.user.id).update_record(inventory=current_inv)
            session.flash = (buyItem.name) + " has been purchased!"
            session.shop_items.remove(buyItem.id)
            db(db.for_sale.item == buyItem.id).delete()
            redirect(URL('shop'))
    if goPrevious.process(formname='go_previous').accepted:
        redirect(URL('shop'))

    return dict(buyItem=buyItem, cost=cost, buyNow=buyNow, goPrevious=goPrevious)

#profile page
@auth.requires_login()
def profilePage():
    current_user = db.auth_user(auth.user.id)
    update_cost = FORM('Cost to Hire: ',
                       INPUT(_name='amount', _type='number',
                             _value=current_user.cost_to_hire,
                             requires=IS_INT_IN_RANGE(minimum=10,maximum=100000,error_message="Invalid cost")),
                       INPUT(_type='submit', _value='UPDATE COST'))
    if update_cost.process().accepted:
        new_cost = update_cost.vars.amount
        current_user.update_record(cost_to_hire=new_cost)
        session.flash = 'Updated cost to hire'
        redirect(URL("profilePage"))
        
    if request.args(0) == 'equip': #equipping items to current loadout
        equipped = db.equip_items(request.args(1, cast=int)) or redirect(URL('profilePage'))
        #if item isn't in inventory, redirect
        if not equipped.id in current_user.inventory:
            redirect(URL('profilePage'))
        if not current_user.curr_loadout: #if first loadout, make new loadout
            new_loadout = db.loadouts.insert()
            current_user.update_record(curr_loadout=new_loadout)
        new_equip_list = current_user.curr_loadout.equip_list or [0]*10
        new_equip_list[equipped.category] = equipped
        current_user.curr_loadout.update_record(equip_list=new_equip_list)
        session.flash = 'Equipped ' + equipped.name
        redirect(URL("profilePage"))

    if request.args(0) == 'unequip': #unequipping items from current loadout
        unequipped = db.equip_items(request.args(1, cast=int)) or redirect(URL('profilePage'))
        new_equip_list = current_user.curr_loadout.equip_list 
        new_equip_list[unequipped.category] = 0
        current_user.curr_loadout.update_record(equip_list=new_equip_list)
        session.flash = 'Unequipped ' + unequipped.name
        redirect(URL("profilePage"))

    if request.args(0) == 'sell': #selling items from inventory
        sold = db.equip_items(request.args(1, cast=int)) or redirect(URL('profilePage'))
        #if item isn't in inventory, redirect
        if not sold.id in current_user.inventory:
            redirect(URL('profilePage'))
        #add gold from sale
        new_gold = current_user.gold + int(sold.cost*.9)
        current_user.update_record(gold=new_gold)
        #actually remove item from inventory
        new_inventory = current_user.inventory
        new_inventory.pop(new_inventory.index(sold.id))
        current_user.update_record(inventory=new_inventory)
        new_rarity = sold.attack + sold.defense + sold.speed
        #insert into table that stores items to be sold
        db.for_sale.insert(item=sold.id, rarity=new_rarity)
        session.flash = 'Sold ' + sold.name
        redirect(URL("profilePage"))

    return dict(update_cost=update_cost, current_user=current_user)

def getItem():
    item = db.equip_items(request.args(0))
    js_string = "jQuery('#display_name').text(%s);" % repr(item.name)
    show_cost = str(int(item.cost*0.9)) + "G"
    js_string += "jQuery('#display_cost').text(%s);" % repr(show_cost)
    show_type = db.equip_types(item.category).name
    js_string += "jQuery('#display_type').text(%s);" % repr(show_type)
    show_atk = str(item.attack)
    js_string += "jQuery('#display_atk').text(%s);" % repr(show_atk)
    show_def = str(item.defense)
    js_string += "jQuery('#display_def').text(%s);" % repr(show_def)
    show_spd = str(item.speed)
    js_string+= "jQuery('#display_spd').text(%s);" % repr(show_spd)
    js_string+= "jQuery('#display_flav').text(%s);" % repr(item.details)
    return js_string
    
def user():
    if request.args(0) == 'profile':
        redirect(URL('profilePage'))
    return dict(form=auth())
