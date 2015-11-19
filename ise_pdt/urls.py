from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^logtime$', views.logtime, name='logtime'),
    url(r'^developer/(?P<username>[a-zA-Z0-9]{3,20})/$', views.index, name='index'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/$', views.index_m, name='index_m'),
    url(r'^developer/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/$', views.project, name='project'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/$', views.project_m, name='project_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/(?P<iteration_id>[0-9]+)/$', views.iteration_m, name='iteration_m'),
    
]
