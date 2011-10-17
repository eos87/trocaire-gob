# -*- coding: utf-8 -*-
from django import forms
from trocaire.models import *

class ProyectoForm(forms.Form):
    organizacion = forms.ModelChoiceField(queryset=Organizacion.objects.all())