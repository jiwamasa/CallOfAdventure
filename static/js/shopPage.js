jQuery(document).ready(function(){
  jQuery(".item").click(function(){
    jQuery("#buy_form").show();
    jQuery("#buy_form").attr("item_id",jQuery(this).attr("id"))
    ajax('/callofadventure/default/itemInfo/'+jQuery(this).attr("id"), [], ':eval');
  });
  jQuery("#buy_form").hide();
});
