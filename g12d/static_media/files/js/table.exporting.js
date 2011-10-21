jQuery.cookie=function(d,c,a){if(typeof c!="undefined"){a=a||{};if(c===null)c="",a.a=-1;var b="";if(a.a&&(typeof a.a=="number"||a.a.toUTCString))typeof a.a=="number"?(b=new Date,b.setTime(b.getTime()+a.a*864E5)):b=a.a,b="; expires="+b.toUTCString();document.cookie=[d,"=",encodeURIComponent(c),b,a.path?"; path="+a.path:"",a.domain?"; domain="+a.domain:"",a.b?"; secure":""].join("")}else{c=null;if(document.cookie&&document.cookie!=""){a=document.cookie.split(";");for(b=0;b<a.length;b++){var e=jQuery.trim(a[b]); if(e.substring(0,d.length+1)==d+"="){c=decodeURIComponent(e.substring(d.length+1));break}}}return c}};

function exportarXLS(id){
	var foo = $('#'+id).html();
	var csrf_token =  $.cookie('csrftoken');
		
	var form = $('<form>').attr({
	    type: 'hidden',
	    method: 'POST',
	    action: '/xls/',
	    id: 'formxls'
	}).appendTo('body');
	
	$('<input>').attr({type: 'hidden', name: 'tabla',  value: foo}).appendTo(form);
	$('<input>').attr({type: 'hidden', name: 'csrfmiddlewaretoken',  value: csrf_token}).appendTo(form);
		
	$(form).submit();
}