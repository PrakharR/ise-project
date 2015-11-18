from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    creating_user = models.ForeignKey(User)
    project_name = models.CharField(max_length=20)
    project_creation_date = models.DateTimeField('date published')
    project_total_time = models.IntegerField(default=0)
    project_yield = models.FloatField(default=0)
    project_description = models.CharField(max_length=600)
    #project_members = models.ManyToManyField(User, through='Assignment') 
    def __str__(self):              # __unicode__ on Python 2
        return self.project_name

class TimeLog(models.Model):
    WORK_CHOICE = (
        ('DEV', 'Development'),
        ('DEF', 'Defect removal'),
        ('MAN', 'Management'),
    )
    #assignment = models.ForeignKey(Assignment)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    log_creation_date = models.DateTimeField('date published')
    time_worked = models.DurationField()
    work_type = models.CharField(max_length=3,choices=WORK_CHOICE,default='DEV')
    def __str__(self):              # __unicode__ on Python 2
        return self.work_type

class Phase(models.Model):
    STATUS_CHOICE = (
        ('ACT', 'Active'),
        ('CLS', 'Closed'),
        ('PND', 'Pending'),
    )
    PHASE_CHOICE = (
        ('INCP', 'Inception'),
        ('ELAB', 'Elaboration'),
        ('CONS', 'Sonstruction'),
        ('TRAN', 'Transition'),
    )
    project = models.ForeignKey(Project)
    phase_name = models.CharField(max_length=4,choices=PHASE_CHOICE)
    phase_start_date = models.DateTimeField('date published')
    phase_status = models.CharField(max_length=3,choices=STATUS_CHOICE)
    def __str__(self):              # __unicode__ on Python 2
        return self.phase_name

class Iteration(models.Model):
    STATUS_CHOICE = (
        ('ACT', 'Active'),
        ('CLS', 'Closed'),
        ('PND', 'Pending'),
    )
    project = models.ForeignKey(Project)
    phase = models.ForeignKey(Phase)
    iteration_name = models.CharField(max_length=20)
    iteration_start_date = models.DateTimeField('date published')
    iteration_status = models.CharField(max_length=3,choices=STATUS_CHOICE)
    iteration_estimate_SLOC = models.IntegerField(default=0)
    iteration_SLOC = models.IntegerField(default=0)
    iteration_estimate_effort = models.FloatField()
    iteration_effort = models.FloatField()
    iteration_defect_injected = models.IntegerField(default=0)
    iteration_defect_removed = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return self.iteration_name