from django.conf.urls import url

from . import views

app_name = 'adminBases'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'disponivel/$', views.disponivel, name='disponivel'),
    url(r'disponivel/selecionar/$', views.disponivel, name='disponivel'),
    #url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]