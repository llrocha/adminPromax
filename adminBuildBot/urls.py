from django.conf.urls import url

from . import views

app_name = 'adminBuildBot'
urlpatterns = [
    url(r'configuracao/(?P<file>.*)/$', views.configuracao, name='configuracao'),
    url(r'configuracao/$', views.configuracao, name='configuracao'),
    url(r'controle/(?P<command>.*)/$', views.controle, name='controle'),
    url(r'controle/$', views.controle, name='controle'),
    #url(r'instancias/$', views.instancias, name='instancias'),
    url(r'logs/(?P<instance>.*)/(?P<file>.*)/$', views.logs, name='logs'),
    url(r'logs/(?P<instance>.*)/$', views.logs, name='logs'),
    url(r'logs/$', views.logs, name='logs'),
    url(r'status/$', views.status, name='status'),
    url(r'', views.index, name='index'),
    #url(r'^$', views.index, name='index'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]