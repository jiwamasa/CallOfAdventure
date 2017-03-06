jQuery(document).ready(function(){
  jQuery('#equip_form').hide();
  jQuery('#sell_form').hide();
  jQuery('.inv_item_name').each(function() {
    $(this).css('font-size', (80/$(this).width())*12);
  });
});

function updateInspector(item_id, isEquipped) {
    ajax('/callofadventure/default/getItem/'+String(item_id), [], ':eval');
    var eq_url = 'profilePage/equip/' + String(item_id);
    var sell_url = 'profilePage/sell/' + String(item_id);
    if (!(isEquipped)) {
	jQuery('#equip_form').show();
	jQuery('#equip_form').prop('action', eq_url);
	jQuery('#sell_form').show();
	jQuery('#sell_form').prop('action', sell_url);
    } else {
	jQuery('#equip_form').hide();
	jQuery('#sell_form').hide();
    }
}
