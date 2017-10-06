from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse

from controlServer.controlclient import ExecuteRemoteCommand
# Create your views here.

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    branches = ExecuteRemoteCommand('90.0.2.174', 9999, 'BuildBotControls->list_branches')
    branches = branches.split(';')

    return render(
        request,
        'adminGit/index.html',
        {
            'menu': 'adminGit',
            'appname': 'adminPromax',
            'title': 'adminGit/Index',
            'year': datetime.now().year,
            'request': request,
            'branches': branches,
            'user': '',
            'password': '',
            'github': 'https://github.com/hbsistec/2A.git',
            'branch': 'master',
        }
    )

def configuracao(request, branch = ''):
    """Renders the 'configuracao' page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'adminGit/index.html',
        {
            'menu': 'adminGit',
            'appname': 'adminPromax',
            'title': 'adminGit/Index',
            'year': datetime.now().year,
            'request': request,
            'user': request.POST.get('user', ''),
            'password': request.POST.get('password', ''),
            'github': request.POST.get('github', 'https://github.com/hbsistec/2A.git'),
            'branch': branch,
            'branches': [branch],
        }
    )