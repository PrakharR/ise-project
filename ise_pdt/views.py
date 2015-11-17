from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import User, Project, TimeLog

def index(request, user_name):
    list_of_projects = Project.objects.filter(user_in_project = user_name).order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'user_name': user_name}
    return render(request, 'ise_pdt/index.html', context)

def project(request, user_name, project_id):
    the_project = Project.objects.filter(id = project_id)
    the_user = User.objects.filter(user_name = user_name)
    list_of_projects = Project.objects.filter(user_in_project = user_name).order_by('project_creation_date')

    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user}
    return render(request, 'ise_pdt/project.html', context)
