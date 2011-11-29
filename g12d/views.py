# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from trocaire.models import *
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    organizaciones = Organizacion.objects.all()
    return render_to_response('index.html', RequestContext(request, locals()))