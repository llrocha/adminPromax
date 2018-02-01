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


def selecionar(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    geo = context['geo']
    server = context['server']
    port = int(context['port'])

    if('dat' in request.POST.keys()):
        selected = ExecuteRemoteCommand(server, port, 'DataBaseControls->mount_dat->' + geo + '->' + request.POST['dat'])
    else:
        selected = 'O sistema de arquivos selecionado não foi montado.'

    context.update({
            'menu':'adminBases',
            'appname':'adminPromax',
            'title':'adminBases/Disponivel',
            'year':datetime.now().year,
            'request':request,
            'selected': selected,
        })

    return render(
        request,
        'adminBases/selecionado.html',
        context
    )