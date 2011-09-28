# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *
from django import forms

class ResultadoInline(admin.TabularInline):
    model = Resultado
    extra = 1
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # This method will turn all TextFields into giant TextFields
        if isinstance(db_field, models.TextField):
            return forms.CharField(label=u'Descripción', 
                                   widget=forms.Textarea(attrs={'cols': 60, 'rows':4, 'class': 'docx'}))
        return super(ResultadoInline, self).formfield_for_dbfield(db_field, **kwargs)


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'organizacion', 'inicio', 'finalizacion', 'contacto']
    filter_horizontal = ['municipios']
    inlines = [ResultadoInline, ]
    
#    formfield_overrides = {
#        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
#        models.TextField: {'widget': forms.Textarea(attrs={'rows':2, 'cols':40})},
#    }


admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Resultado)