from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse
# Create your views here.
from adminClasses.adminClasses import BaseView

from controlServer.controlclient import ExecuteRemoteCommand

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    geo = context['geo']
    server = context['server']
    port = int(context['port'])

    instancias = ExecuteRemoteCommand(server, port, 'BaseControls->instances->' + geo)
    instancias = instancias.split(';')
    
    context.update({
            'menu':'adminPromax',
            'appname':'adminPromax',
            'title':'adminPromax/Index',
            'year':datetime.now().year,
            'request':request,
            'instancias': instancias,
        })

    return render(
        request,
        'adminPromax/index.html',
        context
    )

def contato(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    context.update({
            'menu':'contato',
            'appname':'adminPromax',
            'title':'adminPromax/Contato',
            'year':datetime.now().year,
            'request':request,
        })

    return render(
        request,
        'adminPromax/contato.html',
        context
    )

def sobre(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    context.update({
            'menu':'sobre',
            'appname':'adminPromax',
            'title':'adminPromax/Sobre',
            'year':datetime.now().year,
            'request':request,
        })

    return render(
        request,
        'adminPromax/sobre.html',
        context
    )