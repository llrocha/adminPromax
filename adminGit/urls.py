from django.conf.urls import url

from . import views

app_name = 'adminGit'
urlpatterns = [
    url(r'configuracao/$', views.configuracao, name='configuracao'),
    url(r'branch/(?P<branch>.*)', views.configuracao, name='configuracao'),
    url(r'', views.index, name='index'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]