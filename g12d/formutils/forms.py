from django.utils.encoding import StrAndUnicode
from django.utils.safestring import mark_safe
from django import forms
from django.utils import simplejson

class Foo(StrAndUnicode):
    def __init__(self, foo=None, selected_items=None, load_items=None, **kwargs):
        if foo:            
            self._load_items = simplejson.dumps(load_items)
            self._selected_items = simplejson.dumps(selected_items)       
            self._data = foo.__dict__['config']                        
            
    def __unicode__(self):                 
        return mark_safe(CODE % (self._data, self._load_items, self._selected_items))
        
class FormFKAutoFill(forms.Form):        
    def _foo(self):        
        a = getattr(self, 'Foo')
        selected_items = {}
        load_items = {}
        #verify if form has post data
        if self.data:
            raw_data = checkParams(self.data)
            for val in a.__dict__['config']:
                #separate the elements to load and fill
                select_key = val['fill']['field']
                load_key = val['on_change']['field']
                if raw_data[select_key]:
                    selected_items[select_key] = raw_data[select_key]
                try:
                    if raw_data[load_key]:
                        load_items[load_key] = raw_data[load_key]
                except:
                    pass                
                                                     
        return Foo(foo=a, selected_items=selected_items, load_items=load_items)
    
    #form property
    foo = property(_foo)
    
checkParams = lambda x: dict((k, v) for k,v in x.items() if x[k])
    
CODE = u'''<script type="text/javascript">
        checkjQuery();
        var data = %s;            
        var load_items = %s;
        var selected_items = %s;
        $(document).ready(function(){
            $.each(data, function(index, item){
                var current_select = item.on_change.field;
                var current_fill = item.fill.field;
                
                var elem = $('#id_'+current_select);
                var dest = $('#id_'+current_fill);
                                
                //que pasa aca cuando el form recarga
                if(load_items.hasOwnProperty(current_select)){                    
                    if(selected_items.hasOwnProperty(current_fill)){
                        var sel = selected_items[current_fill];                                                                   
                    }
                    loadData(item, elem, dest, sel);
                }                                
                
                //clean on start
                $(dest).html('');
                $('<option></option>').html('---------').appendTo($(dest));                                
                $(elem).change(function(){                    
                    if($(elem).val()!=''){
                        loadData(item, elem, dest, '');
                    }                   
                });
            });                        
        });
        function loadData(item, elem, dest, sel){            
            $.get('/fillout/?app='+item.fill.app_label
                +'&model='+item.fill.model
                +'&val='+$(elem).val()
                +'&filter='+item.values.filter
                +'&regress='+item.values.regress,                  
                function(info){
                    $(dest).html('');
                    $('<option></option>').html('---------').appendTo($(dest));
                    $.each(info, function(i, obj){
                        var valor = eval('obj.'+item.values.regress.split(',')[0]);
                        var option = $('<option></option>')
                        .val(valor)
                        .html(eval('obj.'+item.values.regress.split(',')[1]))
                        if(valor==sel){
                            $(option).attr('selected', 'selected');
                        }
                        $(option).appendTo($(dest));
                    });                    
            });
        }
        
        function checkjQuery(){
            try{
                var jqueryIsLoaded=jQuery;                
            }
            catch(err){
                alert('jQuery is required :D');
            }
        }                
        </script>'''