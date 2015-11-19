from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Project, TimeLog, Phase, Iteration
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


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

@csrf_exempt
def logtime (request):
  total_project_time_seconds = 0
  username = project = work_type = ''
  if request.POST:
    username = request.POST['user']
    user = User.objects.get(username=username)
    projectid = request.POST['project']
    project = Project.objects.get(id=projectid)
    time = int(request.POST['time_worked'])
    work_type = request.POST['work_type']
    time_worked = timedelta(seconds=time)
    l = TimeLog(user=user,project=project,log_creation_date=timezone.now(),time_worked=time_worked,work_type=work_type)
    l.save()
  
  #Updating total_time parameter of all projects
  list_of_projects = Project.objects.all()  
  for project in list_of_projects:
    total_project_time_seconds = 0
    list_of_project_logs = TimeLog.objects.filter(project = project)
    for projectlog in list_of_project_logs:
      total_project_time_seconds += projectlog.time_worked.seconds
    project.project_total_time = total_project_time_seconds
    project.save()
  
  return HttpResponse('')
  
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
    
    #Variables to store total time
    overall_total_project_time_seconds = 0
    overall_total_project_time_minutes = 0
    overall_total_project_time_hours = 0
    total_project_time_seconds = 0
    total_project_time_minutes = 0
    total_project_time_hours = 0
    total_dev_time_seconds = 0
    total_dev_time_minutes = 0
    total_dev_time_hours = 0
    total_def_time_seconds = 0
    total_def_time_minutes = 0
    total_def_time_hours = 0
    total_man_time_seconds = 0
    total_man_time_minutes = 0
    total_man_time_hours = 0
    
    #getting project and user
    the_project = Project.objects.get(id = project_id)
    the_user = User.objects.get(username = username)
    overall_total_project_time_seconds = the_project.project_total_time
    
    #lists for projects and user's logs
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    list_of_project_logs = TimeLog.objects.filter(project = the_project).filter(user=the_user)
    list_of_dev_logs = TimeLog.objects.filter(project = the_project).filter(user=the_user).filter(work_type='DEV')
    list_of_def_logs = TimeLog.objects.filter(project = the_project).filter(user=the_user).filter(work_type='DEF')
    list_of_man_logs = TimeLog.objects.filter(project = the_project).filter(user=the_user).filter(work_type='MAN')
    
    
    #Adding total user's seconds for project
    for projectlog in list_of_project_logs:
      total_project_time_seconds += projectlog.time_worked.seconds
    
    #Adding total user's seconds for DEV tab
    for devlog in list_of_dev_logs:
      total_dev_time_seconds += devlog.time_worked.seconds
      
    #Adding total user's seconds for DEF tab
    for deflog in list_of_def_logs:
      total_def_time_seconds += deflog.time_worked.seconds
      
    #Adding total user's seconds for MAN tab
    for manlog in list_of_man_logs:
      total_man_time_seconds += manlog.time_worked.seconds
    
    
    #Getting overall Seconds, Minutes and Hours for project
    overall_total_project_time_hours = int(overall_total_project_time_seconds/3600)
    overall_total_project_time_minutes = int(overall_total_project_time_seconds/60)    
    overall_total_project_time_seconds = int(overall_total_project_time_seconds % 60)
      
    #Getting user's Seconds, Minutes and Hours for project
    total_project_time_hours = int(total_project_time_seconds/3600)
    total_project_time_minutes = int(total_project_time_seconds/60)    
    total_project_time_seconds = int(total_project_time_seconds % 60)
    
    #Getting user's Seconds, Minutes and Hours for DEV tab
    total_dev_time_hours = int(total_dev_time_seconds/3600)
    total_dev_time_minutes = int(total_dev_time_seconds/60)    
    total_dev_time_seconds = int(total_dev_time_seconds % 60)
    
    #Getting user's Seconds, Minutes and Hours for DEF tab
    total_def_time_hours = int(total_def_time_seconds/3600)
    total_def_time_minutes = int(total_def_time_seconds/60)    
    total_def_time_seconds = int(total_def_time_seconds % 60)
    
    #Getting user's Seconds, Minutes and Hours for MAN tab
    total_man_time_hours = int(total_man_time_seconds/3600)
    total_man_time_minutes = int(total_man_time_seconds/60)    
    total_man_time_seconds = int(total_man_time_seconds % 60)

    
    #Fixing output to html with leading zeroes for overall project
    if overall_total_project_time_seconds < 10:
      overall_total_project_time_seconds = '0'+str(overall_total_project_time_seconds)
      
    if overall_total_project_time_minutes < 10:
      overall_total_project_time_minutes = '0'+str(overall_total_project_time_minutes)
      
    if overall_total_project_time_hours < 10:
      overall_total_project_time_hours = '0'+str(overall_total_project_time_hours)
    
    #Fixing output to html with leading zeroes for project
    if total_project_time_seconds < 10:
      total_project_time_seconds = '0'+str(total_project_time_seconds)
      
    if total_project_time_minutes < 10:
      total_project_time_minutes = '0'+str(total_project_time_minutes)
      
    if total_project_time_hours < 10:
      total_project_time_hours = '0'+str(total_project_time_hours)
    
    #Fixing output to html with leading zeroes for DEV tab
    if total_dev_time_seconds < 10:
      total_dev_time_seconds = '0'+str(total_dev_time_seconds)
      
    if total_dev_time_minutes < 10:
      total_dev_time_minutes = '0'+str(total_dev_time_minutes)
      
    if total_dev_time_hours < 10:
      total_dev_time_hours = '0'+str(total_dev_time_hours)
      
    #Fixing output to html with leading zeroes for DEF tab
    if total_def_time_seconds < 10:
      total_def_time_seconds = '0'+str(total_def_time_seconds)
      
    if total_def_time_minutes < 10:
      total_def_time_minutes = '0'+str(total_def_time_minutes)
      
    if total_def_time_hours < 10:
      total_def_time_hours = '0'+str(total_def_time_hours)
      
    #Fixing output to html with leading zeroes for MAN tab
    if total_man_time_seconds < 10:
      total_man_time_seconds = '0'+str(total_man_time_seconds)
      
    if total_man_time_minutes < 10:
      total_man_time_minutes = '0'+str(total_man_time_minutes)
      
    if total_man_time_hours < 10:
      total_man_time_hours = '0'+str(total_man_time_hours)
    
    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user, 'total_dev_time_seconds': total_dev_time_seconds, 'total_dev_time_minutes': total_dev_time_minutes, 'total_dev_time_hours': total_dev_time_hours, 'total_def_time_seconds': total_def_time_seconds, 'total_def_time_minutes': total_def_time_minutes, 'total_def_time_hours': total_def_time_hours, 'total_man_time_seconds': total_man_time_seconds, 'total_man_time_minutes': total_man_time_minutes, 'total_man_time_hours': total_man_time_hours, 'total_project_time_seconds': total_project_time_seconds, 'total_project_time_minutes': total_project_time_minutes, 'total_project_time_hours': total_project_time_hours, 'overall_total_project_time_seconds': overall_total_project_time_seconds, 'overall_total_project_time_minutes': overall_total_project_time_minutes, 'overall_total_project_time_hours': overall_total_project_time_hours}
    if request.user.is_authenticated() and request.user.groups.filter(name='Developer').exists():
      return render(request, 'ise_pdt/project.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
  
  
def project_m(request, username, project_id):
    the_project = Project.objects.get(id = project_id)
    the_user = User.objects.get(username = username)
    
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