jQuery(document).ready(function(){
  jQuery(".item").click(function(){
    jQuery("#item_info").show();
    jQuery("#attack").text("Attack: "+jQuery(this).attr("atk"));
    jQuery("#defense").text("Defense: "+jQuery(this).attr("def"));
    jQuery("#speed").text("Speed: "+jQuery(this).attr("spd"));
    jQuery("#cost").text("Cost: "+jQuery(this).attr("cost"));
    
    jQuery("#buy_form").attr("item_id",jQuery(this).attr("id"))
  });
  jQuery("#buy_form").click(function(){
        ajax('/callofadventure/default/buyItem/'+jQuery(this).attr("item_id"), [], ':eval');
    });
  jQuery("#item_info").hide();
});
