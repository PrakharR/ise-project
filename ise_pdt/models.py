from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_email = models.CharField(max_length=100)
    user_password = models.CharField(max_length=20)

    def __str__(self):              # __unicode__ on Python 2
        return self.user_name


class Project(models.Model):
    creating_user = models.ForeignKey(User)
    project_name = models.CharField(max_length=20)
    project_creation_date = models.DateTimeField('date published')
    project_total_time = models.IntegerField(default=0)
    user_in_project = models.CharField(max_length=20)
    def __str__(self):              # __unicode__ on Python 2
        return self.project_name


class TimeLog(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    log_creation_date = models.DateTimeField('date published')
    time_worked = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.time_worked
