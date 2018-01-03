from django.http import HttpRequest
#from django.views.generic.base import TemplateView


from adminConfig.models import Config

class BaseView:
    def __init__(self, request):
        assert isinstance(request, HttpRequest)
        self.request = request

    def context(self):
        context = {}
        url = self.request.META['PATH_INFO']
        breadcrumb = url.strip('/').split('/')
        while(breadcrumb.count('') > 0):
            breadcrumb.remove('')
        context['breadcrumb'] = breadcrumb
        for item in Config.objects.all():
            context[item.key] = item.value
            
        return context

