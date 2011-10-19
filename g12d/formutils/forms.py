from django.utils.encoding import StrAndUnicode
from django.utils.safestring import mark_safe
from django import forms

class Foo(StrAndUnicode):
    def __init__(self, foo=None, **kwargs):        
        if foo:
            self._data = foo.__dict__['config']            
            
    def __unicode__(self):                 
        return mark_safe(u'''<script type="text/javascript">
        $(document).ready(function(){
            var data = %s;            
            $.each(data, function(index, item){
                $('#id_'+item.on_change.field).change(function(){
                    $.get('/fillout/?app='+item.on_change.app_label+'&model='+item.on_change.model,
                        function(){
                            console.log('funca');
                        }
                    );
                });
            });            
        });                
        </script>''' % self._data)
        
class FormFKAutoFill(forms.Form):
    def _foo(self):       
        a = getattr(self, 'Foo')                 
        return Foo(a)
    
    foo = property(_foo)