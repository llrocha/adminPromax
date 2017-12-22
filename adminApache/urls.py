from django.conf.urls import url

from . import views

app_name = 'adminApache'
urlpatterns = [
    url(r'logs/(?P<file>.*)/$', views.logs, name='logs'),
    url(r'logs/$', views.logs, name='logs'),    
    url(r'configuracao/(?P<file>.*)/$', views.configuracao, name='configuracao'),
    url(r'configuracao/$', views.configuracao, name='configuracao'),
    url(r'controle/(?P<command>.*)/$', views.controle, name='controle'),
    url(r'controle/$', views.controle, name='controle'),
    url(r'status/$', views.status, name='status'),
    url(r'^$', views.index, name='index'),
    #url(r'configuracao/(?P<file>[a-zA-Z0-9_.-]+)/$', views.configuracao, name='configuracao'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]
