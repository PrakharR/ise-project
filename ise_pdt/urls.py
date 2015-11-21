from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^logtime$', views.logtime, name='logtime'),
    url(r'^developer/(?P<username>[a-zA-Z0-9]{3,20})/$', views.index, name='index'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/$', views.index_m, name='index_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/createproject/$', views.create_project_m, name='create_project_m'),
    url(r'^developer/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/$', views.project, name='project'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/$', views.project_m, name='project_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/editproject/$', views.edit_project_m, name='edit_project_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/deleteproject/$', views.delete_project_m, name='delete_project_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/createiteration/$', views.create_iteration_m, name='create_iteration_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/(?P<iteration_id>[0-9]+)/$', views.iteration_m, name='iteration_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/(?P<iteration_id>[0-9]+)/edititeration/$', views.edit_iteration_m, name='edit_iteration_m'),
    url(r'^manager/(?P<username>[a-zA-Z0-9]{3,20})/(?P<project_id>[0-9]+)/(?P<iteration_id>[0-9]+)/deleteiteration/$', views.delete_iteration_m, name='delete_iteration_m'),
    
]
