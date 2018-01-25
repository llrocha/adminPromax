from django.conf.urls import url

from . import views

app_name = 'adminEnviron'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'construcao/(?P<geo>.*)$', views.build_promax, name='build_promax'),
    url(r'instancias/(?P<geo>.*)$', views.instancias, name='instancias'),
    url(r'visualizacao/(?P<dir>.*)$', views.visualizacao, name='visualizacao'),
    url(r'monitoramento/$', views.monitoramento, name='monitoramento'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]