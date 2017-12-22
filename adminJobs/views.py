from django.shortcuts import get_object_or_404, render

from datetime import datetime
from django.views import generic
from django.http import HttpRequest, HttpResponse
# Create your views here.

from adminClasses.adminClasses import BaseView

def index(request):
    """Renders the 'index' page."""
    assert isinstance(request, HttpRequest)

    context = BaseView(request).context()
    context.update({
            'menu':'adminJobs',
            'appname':'adminPromax',
            'title':'adminJobs/Index',
            'year':datetime.now().year,
            'request':request,
        })
        
    return render(
        request,
        'adminJobs/index.html',
        context
    )