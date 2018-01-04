from django.shortcuts import get_object_or_404, render

from pygments import highlight
from pygments.lexers import ApacheConfLexer
from pygments.formatters import HtmlFormatter

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse

from adminClasses.adminClasses import BaseView

from controlServer.controlclient import ExecuteRemoteCommand

# Create your views here.

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    context.update({
        'menu':'adminApache',
        'appname':'adminPromax',
        'title':'adminApache/Index',
        'year':datetime.now().year,
        'request':request,
        'errors': [{
            'type': 'danger', 
            'title': 'Apache inativo!', 
            'message': 'Verificar se o servidor Apache está ativo em: <a href="/apache/controle/" class="alert-link">Controle</a>.'
        }],
    })

    return render(
        request,
        'adminApache/index.html',
        context
    )

def configuracao(request, file = ''):
    """Renders the 'configuracao' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()

    geo = context['geo']
    server = context['server']

    config_files = ExecuteRemoteCommand(server, 9999, 'ApacheControls->config_files->' + geo)
    config_files = config_files.split(';')
    config_files.reverse()
    if(file):
        file_content = ExecuteRemoteCommand(server, 9999, 'ApacheControls->configfile_content->' + geo + '->' + file)
        file_content = highlight(file_content, ApacheConfLexer(), HtmlFormatter())
        file_css = HtmlFormatter().get_style_defs('.highlight')
    else:
        file_content = ''
        file_css = ''

    context.update({
            'menu':'adminApache/configuracao',
            'appname':'adminPromax',
            'title':'adminApache/Configuracao',
            'year':datetime.now().year,
            'request':request,
            'config_files': config_files,
            'file_content': file_content,
            'file_css': file_css,
            'config_file': file,
            'errors': [],
        })

    return render(
        request,
        'adminApache/configuracao.html',
        context
    )

def logs(request, file = ''):
    """Renders the 'configuracao' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()

    geo = context['geo']
    server = context['server']

    config_files = ExecuteRemoteCommand(server, 9999, 'ApacheControls->log_files->' + geo)
    config_files = config_files.split(';')
    config_files.reverse()
    if(file):
        file_content = ExecuteRemoteCommand(server, 9999, 'ApacheControls->logfile_content->' + geo + '->' + file)
        #file_content = highlight(file_content, ApacheConfLexer(), HtmlFormatter())
        #file_css = HtmlFormatter().get_style_defs('.highlight')
    else:
        file_content = ''
        file_css = ''

    context.update({
            'menu':'adminApache/logs',
            'appname':'adminPromax',
            'title':'adminApache/Logs',
            'year':datetime.now().year,
            'request':request,
            'config_files': config_files,
            'file_content': file_content,
            #'file_css': file_css,
            'errors': [],
        })

    return render(
        request,
        'adminApache/logs.html',
        context
    )

def controle(request, command = ''):
    """Renders the 'controle' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()

    geo = context['geo']
    server = context['server']

    if(command):
        config_files = ExecuteRemoteCommand(server, 9999, 'ApacheControls->' + command + '->' + geo)
    
    context.update({
            'menu':'adminApache/controle',
            'appname':'adminPromax',
            'title':'adminApache/Controle',
            'year':datetime.now().year,
            'request':request,
            'command': command,
            'errors': [],
        })

    return render(
        request,
        'adminApache/controle.html',
        context
    )

def status(request):
    """Renders the 'status' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()

    geo = context['geo']
    server = context['server']

    status = ExecuteRemoteCommand(server, 9999, 'ApacheControls->status->' + geo)

    context.update({
            'menu':'adminApache/status',
            'appname':'adminPromax',
            'title':'adminApache/Status',
            'year':datetime.now().year,
            'request':request,
            'status': status,
            'errors': [],
        })

    return render(
        request,
        'adminApache/status.html',
        context
    )
