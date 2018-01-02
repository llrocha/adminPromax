from django.http import HttpRequest
#from django.views.generic.base import TemplateView

class BaseView:
    def __init__(self, request):
        assert isinstance(request, HttpRequest)
        self.request = request

    def context(self):
        url = self.request.META['PATH_INFO']
        breadcrumb = url.strip('/').split('/')
        while(breadcrumb.count('') > 0):
            breadcrumb.remove('')
        context = {'breadcrumb': breadcrumb}

        return context

