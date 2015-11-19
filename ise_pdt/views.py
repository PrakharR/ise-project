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
  
  
def logout_user(request):
  logout(request)
  return HttpResponseRedirect('/ise_pdt/login')

  
def index(request, username):
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'username': username}
    if request.user.is_authenticated() and request.user.groups.filter(name='Developer').exists():
      return render(request, 'ise_pdt/index.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
    
  
def index_m(request, username):
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'username': username}
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/index_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
  

def project(request, username, project_id):
    the_project = Project.objects.filter(id = project_id)
    the_user = User.objects.filter(username = username)
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user}
    if request.user.is_authenticated() and request.user.groups.filter(name='Developer').exists():
      return render(request, 'ise_pdt/project.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
  
  
def project_m(request, username, project_id):
    the_project = Project.objects.filter(id = project_id)
    the_user = User.objects.filter(username = username)
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user}
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/project_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')

    
def iteration_m(request, username, project_id, iteration_id):
    the_project = Project.objects.filter(id = project_id)
    the_user = User.objects.filter(username = username)
    the_iteration = Iteration.objects.filter(id = iteration_id)
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user, 'the_iteration': the_iteration}
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/iteration_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')