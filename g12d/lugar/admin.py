from django.contrib import admin
from models import Departamento, Municipio, Comunidad

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    list_filter = ['nombre']
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ['nombre']

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['nombre','departamento']
    list_filter = ['departamento']
    search_fields = ['nombre']
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)

class ComunidadAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, ** kwargs):
        if request.user.is_superuser:        
            form = super(ComunidadAdmin, self).get_form(request, ** kwargs)
        else:
            form = super(ComunidadAdmin, self).get_form(request, ** kwargs)
            #form.base_fields['municipio'].queryset = Municipio.objects.filter(Proyecto.objects.filter())
        return form 

admin.site.register(Comunidad, ComunidadAdmin)





