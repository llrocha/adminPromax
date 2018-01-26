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
    context.update({
            'menu':'adminBases',
            'appname':'adminPromax',
            'title':'adminBases/Index',
            'year':datetime.now().year,
            'request':request,
        })

    return render(
        request,
        'adminBases/index.html',
        context
    )


def disponivel(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()

    geo = context['geo']
    server = context['server']
    port = int(context['port'])

    available_dat = ExecuteRemoteCommand(server, port, 'DataBaseControls->list_available_dat->' + geo)
    available_dat = available_dat.split()

    context.update({
            'menu':'adminBases',
            'appname':'adminPromax',
            'title':'adminBases/Disponivel',
            'year':datetime.now().year,
            'request':request,
            'available_dat': available_dat,
        })

    return render(
        request,
        'adminBases/disponivel.html',
        context
    )