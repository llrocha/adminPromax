from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse

from controlServer.controlclient import ExecuteRemoteCommand

# Create your views here.

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'adminApache/index.html',
        {
            'menu':'adminApache',
            'appname':'adminPromax',
            'title':'adminApache/Index',
            'year':datetime.now().year,
            'request':request,
        }
    )

def instancias(request):
    """Renders the 'instancias' page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'adminApache/instancias.html',
        {
            'menu':'adminApache/instancias',
            'appname':'adminPromax',
            'title':'adminApache/Index',
            'year':datetime.now().year,
            'request':request,
        }
    )

def configuracao(request, file = ''):
    """Renders the 'configuracao' page."""
    assert isinstance(request, HttpRequest)

    file_content = ExecuteRemoteCommand('90.0.2.174', 9999, 'ApacheControls.status')
    return render(
        request,
        'adminApache/configuracao.html',
        {
            'menu':'adminApache/configuracao',
            'appname':'adminPromax',
            'title':'adminApache/Index',
            'year':datetime.now().year,
            'request':request,
            'config_files': ['httpd.conf', 'httpd-dav.conf', 'httpd-info.conf', 'httpd-php.conf', 'httpd_wsgi.conf'],
            'file_content': file_content
        }
    )



def controle(request):
    """Renders the 'controle' page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'adminApache/controle.html',
        {
            'menu':'adminApache/controle',
            'appname':'adminPromax',
            'title':'adminApache/Index',
            'year':datetime.now().year,
            'request':request,
        }
    )

def status(request):
    """Renders the 'status' page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'adminApache/status.html',
        {
            'menu':'adminApache/status',
            'appname':'adminPromax',
            'title':'adminApache/Index',
            'year':datetime.now().year,
            'request':request,
        }
    )
