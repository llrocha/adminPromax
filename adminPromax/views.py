from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse
# Create your views here.
from controlServer.controlclient import ExecuteRemoteCommand

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    instancias = ExecuteRemoteCommand('90.0.2.174', 9999, 'BaseControls->instances')
    instancias = instancias.split(';')    
    return render(
        request,
        'adminPromax/index.html',
        {
            'menu':'adminPromax',
            'appname':'adminPromax',
            'title':'adminPromax/Index',
            'year':datetime.now().year,
            'request':request,
            'instancias': instancias,
        }
    )

def contato(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'adminPromax/contato.html',
        {
            'menu':'contato',
            'appname':'adminPromax',
            'title':'adminJobs/Index',
            'year':datetime.now().year,
            'request':request,
        }
    )

def sobre(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'adminPromax/sobre.html',
        {
            'menu':'sobre',
            'appname':'adminPromax',
            'title':'adminPromax/Sobre',
            'year':datetime.now().year,
            'request':request,
        }
    )