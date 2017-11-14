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
        'adminEnviron/index.html',
        {
            'menu':'adminEnviron',
            'appname':'adminPromax',
            'title':'adminEnviron/Index',
            'year':datetime.now().year,
            'request':request,
        }
    )


def insert_dict(d, l):
    if(len(l)):
        if(not l[0] in d.keys()):
            d[l[0]] = {}
        d[l[0]] = insert_dict(d[l[0]], l[1:])
    else:
        d = {}
    return d


def create_tree(d, l):
    r = ''
    l += 1
    for k, v in d.items():
        
        if(len(v) > 0):
            r += '{0}<li><a href="#">{1}</a>\n{0}  <ul>'.format('\t'*l, k)
            r += create_tree(v, l)
            r += '{0}  </ul>\n{0}</li>'.format('\t'*l)
        else:
            r += '{0}<li>{1}</li>'.format('\t'*l, k)
    return r


def show_tree(request):
    """Renders the 'controle' page."""
    assert isinstance(request, HttpRequest)
    
    path_list = ExecuteRemoteCommand('90.0.2.174', 9999, 'EnvironControls->environment_tree')
    
    tree = {}    
    
    for path in path_list.split():
        #path = path.split()[0]
        path = path.split('/')
        path.remove('')
        insert_dict(tree, path)
    
    html_tree = create_tree(tree, 0)

    return render(
        request,
        'adminEnviron/index.html',
        {
            'menu':'adminEnviron',
            'appname':'adminPromax',
            'title':'adminEnviron/Index',
            'year':datetime.now().year,
            'request':request,
            'html_tree': html_tree
        }
    )