jQuery(document).ready(function(){
 // jQuery('#hire_form').hide();
});

function updateInspector(employee_id, isPicked) {
    ajax('/callofadventure/default/getUser/'+String(employee_id), [], ':eval');
    var hire_url = 'showHire/' + String(hire);
    
  
  ////      jQuery('#hire_form').show();
       jQuery('#hire_form').prop('action', hire_url);



}
