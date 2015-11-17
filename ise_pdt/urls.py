from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<user_name>[a-zA-Z0-9]{3,16})/$', views.index, name='index'),
    url(r'^(?P<user_name>[a-zA-Z0-9]{3,16})/(?P<project_id>[0-9]+)/$', views.project, name='project'),

]
