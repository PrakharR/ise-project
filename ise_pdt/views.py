from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from .models import Project, TimeLog, Phase, Iteration

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name='Developer').exists():
                  return HttpResponseRedirect('/ise_pdt/developer/'+user.username+'/')
                else:
                  return HttpResponseRedirect('/ise_pdt/manager/'+user.username+'/')
    return render(request, 'ise_pdt/login.html')

def index(request, username):
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'username': username}
    return render(request, 'ise_pdt/index.html', context)
  
def index_m(request, user_name):
    list_of_projects = Project.objects.filter(user_in_project = user_name).order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'user_name': user_name}
    return render(request, 'ise_pdt/index_m.html', context)
  


def project(request, username, project_id):
    the_project = Project.objects.filter(id = project_id)
    the_user = User.objects.filter(username = username)
    list_of_projects = Project.objects.all().order_by('project_creation_date')

    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user}
    return render(request, 'ise_pdt/project.html', context)
  
def project_m(request, user_name, project_id):
    the_project = Project.objects.filter(id = project_id)
    the_user = User.objects.filter(user_name = user_name)
    list_of_projects = Project.objects.filter(user_in_project = user_name).order_by('project_creation_date')

    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user}
    return render(request, 'ise_pdt/project.html', context)
