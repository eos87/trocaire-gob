var dicc;

(function($) {	
	$(document).ready(function(){
		$('#add_id_comunidad').removeAttr('onclick');
		$('#add_id_comunidad').attr('href', '#');
		
		$('#id_municipio').change(function(){
			var val = $(this).val();
			var name = $('#id_municipio option:selected').text();
			if(val!=''){
				dicc = {'id': val, 'name': name}
			}
		});
		$('#add_id_comunidad').click(function(){
			if($('#id_municipio').val()==''){
				alert('Debe seleccionar un municipio');
				return false;
			}
			showCustomPopup(dicc, this);
			return false;
		});
	})
})(jQuery || django.jQuery);

function showCustomPopup(dicc, triggeringLink) {
	var name = triggeringLink.id.replace(/^add_/, '');	
	var href = '/admin/lugar/comunidad/add/?_popup=1&id='+dicc.id+'&name='+dicc.name;
	var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}