from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.models import User

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'creating_user', 'project_creation_date', 
                    'project_total_time', 'project_yield', 'project_description')

class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'log_creation_date', 'time_worked', 'work_type')

class IterationAdmin(admin.ModelAdmin):
    list_display = ('project', 'phase', 'iteration_name', 'iteration_start_date',
    	            'iteration_status', 'iteration_estimate_SLOC', 'iteration_SLOC',
                    'iteration_estimate_effort', 'iteration_effort',
    	            'iteration_defect_injected', 'iteration_defect_removed')

class PhaseAdmin(admin.ModelAdmin):
    list_display = ('project', 'phase_name', 'phase_start_date', 'phase_status')

class DefectAdmin(admin.ModelAdmin):
    list_display = ('defect_type', 'iteration_of_injection', 'description')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'assignment_date')

#class WorkAdmin(admin.ModelAdmin):
#    list_display = ('work_name',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(TimeLog, TimeLogAdmin)
admin.site.register(Iteration, IterationAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Defect, DefectAdmin)
admin.site.register(Assignment, AssignmentAdmin)
#admin.site.register(Work, WorkAdmin)
