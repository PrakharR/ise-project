from django.contrib import admin

# Register your models here.
from .models import User, Project, TimeLog

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_password')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'creating_user', 'project_creation_date', 'project_total_time')

class TimeLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'time_worked')

admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TimeLog, TimeLogAdmin)
