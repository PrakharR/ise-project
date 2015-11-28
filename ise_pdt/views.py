from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Project, TimeLog, Assignment, Phase, Iteration, Defect
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
    
    the_phase = Phase.objects.filter(project=project).get(phase_status='ACT')
    phase = the_phase.phase_name
    
    the_iteration = Iteration.objects.filter(project=project).get(iteration_status='ACT')
    iteration = the_iteration.iteration_name
    
    time = int(request.POST['time_worked'])
    
    work_type = request.POST['work_type']
    time_worked = timedelta(seconds=time)
    
    l = TimeLog(user=user,project=project,phase=phase,iteration=iteration,log_creation_date=timezone.now(),time_worked=time_worked,work_type=work_type)
    l.save()
  
    #Updating total_time parameter of selected projects
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
    
    #added by keisei 26-11-2015
    list_of_iterations = Iteration.objects.filter(project=the_project).order_by('phase', 'iteration_start_date') 
    #added by keisei 26-11-2015
    list_of_defects = Defect.objects.filter(iteration_of_injection__in = list_of_iterations);
    
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
    
    context = {'list_of_projects': list_of_projects, 'list_of_iterations': list_of_iterations, 'list_of_defects': list_of_defects, 'the_project': the_project, 'the_user': the_user, 'total_dev_time_seconds': total_dev_time_seconds, 'total_dev_time_minutes': total_dev_time_minutes, 'total_dev_time_hours': total_dev_time_hours, 'total_def_time_seconds': total_def_time_seconds, 'total_def_time_minutes': total_def_time_minutes, 'total_def_time_hours': total_def_time_hours, 'total_man_time_seconds': total_man_time_seconds, 'total_man_time_minutes': total_man_time_minutes, 'total_man_time_hours': total_man_time_hours, 'total_project_time_seconds': total_project_time_seconds, 'total_project_time_minutes': total_project_time_minutes, 'total_project_time_hours': total_project_time_hours, 'overall_total_project_time_seconds': overall_total_project_time_seconds, 'overall_total_project_time_minutes': overall_total_project_time_minutes, 'overall_total_project_time_hours': overall_total_project_time_hours}
    if request.user.is_authenticated() and request.user.groups.filter(name='Developer').exists():
      return render(request, 'ise_pdt/project.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
  
  
def project_m(request, username, project_id):
    overall_total_project_time_seconds = 0
    overall_total_project_time_minutes = 0
    overall_total_project_time_hours = 0
    
    the_project = Project.objects.get(id = project_id)
    the_user = User.objects.get(username = username)
    overall_total_project_time_seconds = the_project.project_total_time
    the_phase_incp = Phase.objects.filter(project=the_project).get(phase_name='INCP')
    the_phase_elab = Phase.objects.filter(project=the_project).get(phase_name='ELAB')
    the_phase_cons = Phase.objects.filter(project=the_project).get(phase_name='CONS')
    the_phase_tran = Phase.objects.filter(project=the_project).get(phase_name='TRAN')
    
    
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    
    list_of_iterations = Iteration.objects.filter(project=the_project).order_by('phase', 'iteration_start_date')
    list_of_iterations_incp = Iteration.objects.filter(project=the_project).filter(phase = the_phase_incp)
    list_of_iterations_elab = Iteration.objects.filter(project=the_project).filter(phase = the_phase_elab)
    list_of_iterations_cons = Iteration.objects.filter(project=the_project).filter(phase = the_phase_cons)
    list_of_iterations_tran = Iteration.objects.filter(project=the_project).filter(phase = the_phase_tran)
    
    
    
    #Getting overall Seconds, Minutes and Hours for project
    overall_total_project_time_hours = int(overall_total_project_time_seconds/3600)
    overall_total_project_time_minutes = int(overall_total_project_time_seconds/60)    
    overall_total_project_time_seconds = int(overall_total_project_time_seconds % 60)
    
    #Fixing output to html with leading zeroes for overall project
    if overall_total_project_time_seconds < 10:
      overall_total_project_time_seconds = '0'+str(overall_total_project_time_seconds)
      
    if overall_total_project_time_minutes < 10:
      overall_total_project_time_minutes = '0'+str(overall_total_project_time_minutes)
      
    if overall_total_project_time_hours < 10:
      overall_total_project_time_hours = '0'+str(overall_total_project_time_hours)
      
    project_ESLOC = 0
    incp_ESLOC = elab_ESLOC = cons_ESLOC = tran_ESLOC = 0
    
    project_SLOC = 0
    incp_SLOC = elab_SLOC = cons_SLOC = tran_SLOC = 0
    
    project_ETE = 0
    incp_ETE = elab_ETE = cons_ETE = tran_ETE = 0
      
    #METRICS
    #Time Based
    # 1) Estimated Delivered Lines of Code
    #Project
    for projectiteration in list_of_iterations:
      project_ESLOC += projectiteration.iteration_estimate_SLOC
    
    #Phase - Inception
    for projectiteration in list_of_iterations_incp:
      incp_ESLOC += projectiteration.iteration_estimate_SLOC
    
    #Phase - Elaboration
    for projectiteration in list_of_iterations_elab:
      elab_ESLOC += projectiteration.iteration_estimate_SLOC
    #Phase - Construction
    for projectiteration in list_of_iterations_cons:
      cons_ESLOC += projectiteration.iteration_estimate_SLOC
    #Phase - Transition
    for projectiteration in list_of_iterations_tran:
      tran_ESLOC += projectiteration.iteration_estimate_SLOC
    
    # 2) Delivered Lines of Code
    #Project
    for projectiteration in list_of_iterations:
      project_SLOC += projectiteration.iteration_SLOC
    
    project_SLOC_percentage=(1.0*project_SLOC/project_ESLOC)*100
    #Phase - Inception
    for projectiteration in list_of_iterations_incp:
      incp_SLOC += projectiteration.iteration_SLOC
    
    incp_SLOC_percentage=(1.0*incp_SLOC/incp_ESLOC)*100
    
    #Phase - Elaboration
    for projectiteration in list_of_iterations_elab:
      elab_SLOC += projectiteration.iteration_SLOC
    
    elab_SLOC_percentage=(1.0*elab_SLOC/elab_ESLOC)*100
    
    #Phase - Construction
    for projectiteration in list_of_iterations_cons:
      cons_SLOC += projectiteration.iteration_SLOC
    
    cons_SLOC_percentage=(1.0*cons_SLOC/cons_ESLOC)*100
    
    #Phase - Transition
    for projectiteration in list_of_iterations_tran:
      tran_SLOC += projectiteration.iteration_SLOC
    
    tran_SLOC_percentage=(1.0*tran_SLOC/tran_ESLOC)*100
    
    # 3) Estimated Time Effort
    #Project
    for projectiteration in list_of_iterations:
      project_ETE += projectiteration.iteration_estimate_effort
    
    #Phase - Inception
    for projectiteration in list_of_iterations_incp:
      incp_ETE += projectiteration.iteration_estimate_effort
    
    #Phase - Elaboration
    for projectiteration in list_of_iterations_elab:
      elab_ETE += projectiteration.iteration_estimate_effort
    
    
    #Phase - Construction
    for projectiteration in list_of_iterations_cons:
      cons_ETE += projectiteration.iteration_estimate_effort
    
    
    #Phase - Transition
    for projectiteration in list_of_iterations_tran:
      tran_ETE += projectiteration.iteration_estimate_effort
    
    
    # 4) Time Effort
    #Project
    project_TE = ((the_project.project_total_time+1)/2592000)
    project_TE_percentage = (1.0*project_TE/project_ETE) * 100
    #Phase - Inception
    incp_TE = 1
    list_time_incp = TimeLog.objects.filter(project= the_project).filter(phase='INCP')
    
    for log in list_time_incp:
      incp_TE += log.time_worked.seconds
    
    incp_TE = (incp_TE/2592000)
    incp_TE_percentage = (1.0*incp_TE*incp_ETE)*100
    
    #Phase - Elaboration
    elab_TE = 1
    list_time_elab = TimeLog.objects.filter(project= the_project).filter(phase='ELAB')
    
    for log in list_time_elab:
      elab_TE += log.time_worked.seconds
    
    elab_TE = (elab_TE/2592000)
    elab_TE_percentage = (1.0*elab_TE*elab_ETE)*100
    
    #Phase - Construction
    cons_TE = 1
    list_time_cons = TimeLog.objects.filter(project= the_project).filter(phase='CONS')
    
    for log in list_time_cons:
      cons_TE += log.time_worked.seconds
    
    cons_TE = (cons_TE/2592000)
    cons_TE_percentage = (1.0*cons_TE*cons_ETE)*100
    
    #Phase - Transition
    tran_TE = 1
    list_time_tran = TimeLog.objects.filter(project= the_project).filter(phase='TRAN')
    
    for log in list_time_tran:
      tran_TE += log.time_worked.seconds
    
    tran_TE = (tran_TE/2592000)
    tran_TE_percentage = (1.0*tran_TE*tran_ETE)*100
    
    # 5) Productivity
    #Project
    project_productivity = project_SLOC/(project_TE+1)
    
    #Phase - Inception
    incp_productivity = incp_SLOC/(incp_TE+1)
    
    #Phase - Elaboration
    elab_productivity = elab_SLOC/(elab_TE+1)
    
    #Phase - Construction
    cons_productivity = cons_SLOC/(cons_TE+1)
    
    #Phase - Transition
    tran_productivity = tran_SLOC/(tran_TE+1)
    
    #Size Based
    # 1) Number of Defects Injected
    #Project
    project_DI = Defect.objects.filter(iteration_of_injection__in = list_of_iterations).count();
    
    #Phase - Inception
    incp_DI = Defect.objects.filter(iteration_of_injection__in = list_of_iterations_incp).count();
    
    #Phase - Elaboration
    elab_DI = Defect.objects.filter(iteration_of_injection__in = list_of_iterations_elab).count();
    
    #Phase - Construction
    cons_DI = Defect.objects.filter(iteration_of_injection__in = list_of_iterations_cons).count();
    
    #Phase - Transition
    tran_DI = Defect.objects.filter(iteration_of_injection__in = list_of_iterations_tran).count();
    
    # 2) Number of Defects Removed 
    #Project
    project_DR = project_DI
    
    #Phase - Inception
    incp_DR = incp_DI
    
    #Phase - Elaboration
    elab_DR = elab_DI
    
    #Phase - Construction
    cons_DR = cons_DI
    
    #Phase - Transition
    tran_DR = tran_DI
    
    # 3) Defect Injection Rate
    #Project
    project_DIR = project_DI/((project_TE+1)*720)
    
    #Phase - Inception
    incp_DIR = incp_DI/((incp_TE+1)*720)
    
    #Phase - Elaboration
    elab_DIR = elab_DI/((elab_TE+1)*720)
    
    #Phase - Construction
    cons_DIR = cons_DI/((cons_TE+1)*720)
    
    #Phase - Transition
    tran_DIR = tran_DI/((tran_TE+1)*720)
    
    # 4) Defect Removal Rate
    #Project
    project_DRR = project_DI/((int(overall_total_project_time_hours)+1)*720)
    
    #Phase - Inception
    incp_DRR = incp_DI/((incp_TE+1)*720)
    
    #Phase - Elaboration
    elab_DRR = elab_DI/((elab_TE+1)*720)
    
    #Phase - Construction
    cons_DRR = cons_DI/((cons_TE+1)*720)
    
    #Phase - Transition
    tran_DRR = project_DI/((tran_TE+1)*720)
    
    # 5) Defect Density
    #Project
    project_DD = project_DI/(project_SLOC*1000)
    
    #Phase - Inception
    incp_DD = incp_DI/(incp_SLOC*1000)
    
    #Phase - Elaboration
    elab_DD = elab_DI/(elab_SLOC*1000)
    
    #Phase - Construction
    cons_DD = cons_DI/(cons_SLOC*1000)
    
    #Phase - Transition
    tran_DD = tran_DI/(tran_SLOC*1000)
    
    context = {'list_of_projects': list_of_projects, 'list_of_iterations': list_of_iterations, 'the_project': the_project, 'the_user': the_user, 'overall_total_project_time_seconds': overall_total_project_time_seconds, 'overall_total_project_time_minutes': overall_total_project_time_minutes, 'overall_total_project_time_hours': overall_total_project_time_hours,
              'project_DD':project_DD,'incp_DD':incp_DD,'elab_DD':elab_DD,'cons_DD':cons_DD, 'tran_DD': tran_DD,'project_DIR':project_DIR,'incp_DIR':incp_DIR,'elab_DIR':elab_DIR,'cons_DIR':cons_DIR, 'tran_DIR': tran_DIR,'project_DRR':project_DRR,'incp_DRR':incp_DRR,'elab_DRR':elab_DRR,'cons_DRR':cons_DRR, 'tran_DRR': tran_DRR,'project_DR':project_DR,'incp_DR':incp_DR,'elab_DR':elab_DR,'cons_DR':cons_DR, 'tran_DR': tran_DR,'project_DI':project_DI,'incp_DI':incp_DI,'elab_DI':elab_DI,'cons_DI':cons_DI, 'tran_DI': tran_DI,'project_productivity':project_productivity,'incp_productivity':incp_productivity,'elab_productivity':elab_productivity,'cons_productivity':cons_productivity, 'tran_productivity': tran_productivity,'project_ETE':project_ETE,'incp_ETE':incp_ETE,'elab_ETE':elab_ETE,'cons_ETE':cons_ETE, 'tran_ETE': tran_ETE,'project_TE_percentage':project_TE_percentage,'incp_TE_percentage':incp_TE_percentage,'elab_TE_percentage':elab_TE_percentage,'cons_TE_percentage':cons_TE_percentage, 'tran_TE_percentage': tran_TE_percentage,'project_ESLOC':project_ESLOC,'incp_ESLOC':incp_ESLOC,'elab_ESLOC':elab_ESLOC,'cons_ESLOC':cons_ESLOC, 'tran_ESLOC': tran_ESLOC,'project_SLOC_percentage':project_SLOC_percentage,'incp_SLOC_percentage':incp_SLOC_percentage,'elab_SLOC_percentage':elab_SLOC_percentage,'cons_SLOC_percentage':cons_SLOC_percentage, 'tran_SLOC_percentage': tran_SLOC_percentage}
    
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/project_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')


def next_iteration_m(request, username, project_id):
    the_project = Project.objects.get(id = project_id)
    the_phase = Phase.objects.filter(project = the_project).get(phase_status = 'ACT')
    current_active_iteration = Iteration.objects.filter(project=the_project).get(iteration_status='ACT')
    next_active_iteration = current_active_iteration
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    list_of_iterations = Iteration.objects.filter(project=the_project).order_by('phase', 'iteration_start_date')
    
    if request.POST:
      iterationsloc = request.POST['p_iterationSLOC']
      iterationte = request.POST['p_iterationTE']

      for index, item in enumerate(list_of_iterations):
        if item.id == current_active_iteration.id:
          the_index = index
          break

      for index2, item2 in enumerate(list_of_iterations):
        if index2 == (the_index + 1):
          next_active_iteration = item2
          break

      if current_active_iteration == next_active_iteration:
        
        return HttpResponseRedirect('/ise_pdt/manager/'+username+'/'+project_id+'/')
      
      else:
        current_active_iteration.iteration_status = 'CLS'
        current_active_iteration.iteration_SLOC = iterationsloc
        current_active_iteration.iteration_effort = iterationte
        
        next_active_iteration.iteration_status = 'ACT'
        
        phase_to_activate = next_active_iteration.phase

        the_phase.phase_status = 'CLS'
        the_phase.save()

        phase_to_activate.phase_status = 'ACT'
        phase_to_activate.save()

        current_active_iteration.save()
        next_active_iteration.save()
    
        return HttpResponseRedirect('/ise_pdt/manager/'+username+'/'+project_id+'/')
    
    context = {'username': username,'the_project': the_project, 'list_of_projects': list_of_projects}
    
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/next_iteration_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
    
    
    
    
def iteration_m(request, username, project_id, iteration_id):
    the_project = Project.objects.get(id = project_id)
    the_user = User.objects.get(username = username)
    the_iteration = Iteration.objects.get(id = iteration_id)
    
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    
    context = {'list_of_projects': list_of_projects, 'the_project': the_project, 'the_user': the_user, 'the_iteration': the_iteration}
    
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/iteration_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
    
    
    
def create_project_m(request, username):
    the_user = User.objects.get(username=username)
    
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    
    if request.POST:
      projectname = request.POST['projectname']
      projectdescription = request.POST['projectdescription']
      the_project = Project(creating_user=the_user,project_name=projectname,project_creation_date=timezone.now(),project_total_time=0,project_yield=0,project_description=projectdescription,project_active_phase='INCP',project_active_iteration='sample',project_status='PND')
      the_project.save()
      
      #Create 4 Phases
      phase_incp = Phase(project=the_project,phase_name='INCP',phase_start_date=timezone.now(),phase_status='ACT')
      phase_elab = Phase(project=the_project,phase_name='ELAB',phase_start_date=timezone.now(),phase_status='PND')
      phase_cons = Phase(project=the_project,phase_name='CONS',phase_start_date=timezone.now(),phase_status='PND')
      phase_tran = Phase(project=the_project,phase_name='TRAN',phase_start_date=timezone.now(),phase_status='PND')
      phase_incp.save()
      phase_elab.save()
      phase_cons.save()
      phase_tran.save()
      
      #Create Dummy Iteration
      the_iteration = Iteration(project=the_project,phase=phase_incp,iteration_name='INCP1',iteration_start_date=timezone.now(),iteration_status='ACT',iteration_estimate_SLOC=1000,iteration_SLOC=100,iteration_estimate_effort=1,iteration_effort=0,iteration_defect_injected=0,iteration_defect_removed=0)
      the_iteration_elab = Iteration(project=the_project,phase=phase_elab,iteration_name='ELAB1',iteration_start_date=timezone.now(),iteration_status='PND',iteration_estimate_SLOC=1000,iteration_SLOC=100,iteration_estimate_effort=1,iteration_effort=0,iteration_defect_injected=0,iteration_defect_removed=0)
      the_iteration_cons = Iteration(project=the_project,phase=phase_cons,iteration_name='CONS1',iteration_start_date=timezone.now(),iteration_status='PND',iteration_estimate_SLOC=1000,iteration_SLOC=100,iteration_estimate_effort=1,iteration_effort=0,iteration_defect_injected=0,iteration_defect_removed=0)
      the_iteration_tran = Iteration(project=the_project,phase=phase_tran,iteration_name='TRAN1',iteration_start_date=timezone.now(),iteration_status='PND',iteration_estimate_SLOC=1000,iteration_SLOC=100,iteration_estimate_effort=1,iteration_effort=0,iteration_defect_injected=0,iteration_defect_removed=0)

      the_iteration.save()
      the_iteration_elab.save()
      the_iteration_cons.save()
      the_iteration_tran.save()
      
      the_project_id = str(the_project.id)
      
      return HttpResponseRedirect('/ise_pdt/manager/'+the_user.username+'/'+the_project_id+'/')
    
    context = {'username': username, 'list_of_projects': list_of_projects}
    
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/create_project_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
    
    
def edit_project_m(request, username, project_id):
    the_project = Project.objects.get(id=project_id)
    
    if request.POST:
      projectname = request.POST['projectname']
      projectyield = request.POST['projectyield']
      projectdescription = request.POST['projectdescription']
      projectstatus = request.POST['projectstatus']
      
      the_project.project_name = projectname
      the_project.project_yield = projectyield
      the_project.project_description = projectdescription
      the_project.project_status = projectstatus
      
      the_project.save()
    
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return HttpResponseRedirect('/ise_pdt/manager/'+username+'/'+project_id+'/')
    else:
      return HttpResponseRedirect('/ise_pdt/logout')

def delete_project_m(request, username, project_id):
    the_project = Project.objects.get(id=project_id)
    
    Project.objects.get(id=project_id).delete()
    Iteration.objects.filter(project=the_project).delete()
    Phase.objects.filter(project=the_project).delete()
    TimeLog.objects.filter(project=the_project).delete()
    
    return HttpResponseRedirect('/ise_pdt/manager/'+username+'/')
    
    
def create_iteration_m(request, username, project_id):
    the_user = User.objects.get(username=username)
    the_project = Project.objects.get(id=project_id)
    
    list_of_projects = Project.objects.all().order_by('project_creation_date')
    
    if request.POST:
      iterationname = request.POST['iterationname']
      phasename = request.POST['phasename']
      iterationesloc = request.POST['iterationESLOC']
      iterationete = request.POST['iterationETE']
      the_phase = Phase.objects.filter(project=the_project).get(phase_name=phasename)

      the_iteration = Iteration(project=the_project,phase=the_phase,iteration_name=iterationname,iteration_start_date=timezone.now(),iteration_status='PND',iteration_estimate_SLOC=iterationesloc,iteration_SLOC=0,iteration_estimate_effort=iterationete,iteration_effort=0,iteration_defect_injected=0,iteration_defect_removed=0)

      the_iteration.save()

      return HttpResponseRedirect('/ise_pdt/manager/'+the_user.username+'/'+project_id+'/')
    
    context = {'username': username,'the_project': the_project, 'list_of_projects': list_of_projects}
    
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return render(request, 'ise_pdt/create_iteration_m.html', context)
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
  
def edit_iteration_m(request, username, project_id, iteration_id):
    the_iteration = Iteration.objects.get(id=iteration_id)
    
    if request.POST:
      iterationname = request.POST['iterationname']
      the_iteration.iteration_name = iterationname
      the_iteration.save()
    
    if request.user.is_authenticated() and request.user.groups.filter(name='Manager').exists():
      return HttpResponseRedirect('/ise_pdt/manager/'+username+'/'+project_id+'/'+iteration_id+'/')
    else:
      return HttpResponseRedirect('/ise_pdt/logout')
  
  
  
def delete_iteration_m(request, username, project_id, iteration_id):
    the_iteration = Iteration.objects.get(id=iteration_id)
    
    Iteration.objects.get(id=iteration_id).delete()
    TimeLog.objects.filter(iteration=the_iteration.iteration_name).delete()
    
    return HttpResponseRedirect('/ise_pdt/manager/'+username+'/'+project_id+'/')
  
  
@csrf_exempt 
def report_defect(request):
    if request.POST:
      d_type = request.POST['d_type']
      iteration_oi_id = request.POST['iteration_oi']
      d_desc = request.POST['d_desc']

      the_iteration = Iteration.objects.get(id = iteration_oi_id)
      the_defect = Defect(defect_type=d_type,description=d_desc,iteration_of_injection=the_iteration)

      the_defect.save()

    return HttpResponse('')