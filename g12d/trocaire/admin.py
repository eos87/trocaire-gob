# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class OrgAdmin(admin.ModelAdmin):
    list_display = ['nombre_corto', 'contacto', 'telefono', 'direccion']
    search_fields = ['nombre_corto', 'contacto', 'telefono', 'nombre']

admin.site.register(ResultadoPrograma)
admin.site.register(Organizacion, OrgAdmin)