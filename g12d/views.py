# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from trocaire.models import *

def home(request):
    organizaciones = Organizacion.objects.all()
    return render_to_response('index.html', RequestContext(request, locals()))