from django.shortcuts import get_object_or_404, render

from pygments import highlight
from pygments.lexers import PythonLexer
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
            'menu':'adminBuildBot/index',
            'appname':'adminPromax',
            'title':'adminBuildBot/Index',
            'year':datetime.now().year,
            'request':request,
        })

    return render(
        request,
        'adminBuildBot/buildbot.html',
        context
    )


def configuracao(request, file = ''):
    """Renders the 'configuracao' page."""
    assert isinstance(request, HttpRequest)

    config_files = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->config_files')
    config_files = config_files.split(';')
    config_files.reverse()

    file_css = ''
    file_content = ''
    if(file):
        file_content = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->configfile_content->' + file)
        file_content = highlight(file_content, PythonLexer(), HtmlFormatter())
        file_css = HtmlFormatter().get_style_defs('.highlight')

    context = BaseView(request).context()
    context.update({
            'menu':'adminBuildBot/configuracao',
            'appname':'adminPromax',
            'title':'adminBuildBot/Configuração',
            'year':datetime.now().year,
            'request':request,
            'config_files': config_files,
            'file_content': file_content,
            'file_css': file_css,
        })

    return render(
        request,
        'adminBuildBot/configuracao.html',
        context
    )

def logs(request, instance = '', file = ''):
    """Renders the 'configuracao' page."""
    assert isinstance(request, HttpRequest)

    if(file):
        file_content = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->logfile_content->' + instance + '->' + file)
    else:
        file_content = ''
        file_css = ''

    if(instance):
        config_files = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->log_files->' + instance)
        config_files = config_files.split(';')
    else:
        config_files = ''
        instance = 'worker'

    if(instance == 'master'):
        master = 'active'
        worker = ''
    elif(instance == 'worker'):
        master = ''
        worker = 'active'
    else:
        master = ''
        worker = 'active'

    context = BaseView(request).context()
    context.update({
            'menu':'adminBuildBot/logs',
            'appname':'adminPromax',
            'title':'adminBuildBot/Logs',
            'year':datetime.now().year,
            'request':request,
            'config_files': config_files,
            'file_content': file_content,
            'instance': instance,
            'master': master,
            'worker': worker,
        })

    return render(
        request,
        'adminBuildBot/logs.html',
        context
    )

def controle(request, command = ''):
    """Renders the 'controle' page."""
    assert isinstance(request, HttpRequest)
    if(command):
        config_files = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->' + command)

    context = BaseView(request).context()
    context.update({
            'menu':'adminBuildBot/controle',
            'appname':'adminPromax',
            'title':'adminBuildBot/Controle',
            'year':datetime.now().year,
            'request':request,
            'command': command
        })

    return render(
        request,
        'adminBuildBot/controle.html',
        context
    )

def status(request):
    """Renders the 'status' page."""
    assert isinstance(request, HttpRequest)
    status = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->status')

    context = BaseView(request).context()
    context.update({
            'menu':'adminBuildBot/status',
            'appname':'adminPromax',
            'title':'adminBuildBot/Status',
            'year':datetime.now().year,
            'request':request,
            'status': status,
        })
        
    return render(
        request,
        'adminBuildBot/status.html',
        context
    )


def instancias(request):
    """Renders the 'instancias' page."""
    assert isinstance(request, HttpRequest)

    instancias = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->instances')
    instancias = instancias.split(';')

    context = BaseView(request).context()
    context.update({
            'menu':'adminBuildBot/instancias',
            'appname':'adminPromax',
            'title':'adminBuildBot/Instâncias',
            'year':datetime.now().year,
            'request':request,
            'instancias': instancias,
        })

    return render(
        request,
        'adminBuildBot/instancias.html',
        context
    )