from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse
# Create your views here.

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'adminBuildBot/index.html',
        {
            'menu':'adminBuildBot',
            'appname':'adminPromax',
            'title':'adminBuildBot/Index',
            'year':datetime.now().year,
            'request':request,
        }
    )