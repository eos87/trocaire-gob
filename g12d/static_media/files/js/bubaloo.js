(function($) {	
	$(document).ready(function(){
		$('#id_municipio').html('');
		var id = getParameterByName('id');
		var name = getParameterByName('name');
		$('<option></option>').val(id).text(name).appendTo($('#id_municipio'));
	})
})(jQuery || django.jQuery);

function getParameterByName(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.href);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}
