from django.db import models
from django.contrib.auth.models import User

class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        REVIEW = 'review', 'Review'
        DONE = 'done', 'Done'
class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        URGENT = 4, 'Urgent'





class Projects(models.Model):

    project_name = models.CharField(max_length=30) 
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    start_date = models.DateField()
    end_date = models.DateField()

    github_link = models.URLField(null=True, blank=True)

class Tasks(models.Model):
    task_name = models.CharField(max_length=30) 
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField()
    dadeline = models.DateField()
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    project = models.ManyToManyField(Projects, related_name='projects', blank=True, null=True)
class Plans(models.Model):
    plan_name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tasks = models.ForeignKey(Tasks, related_name='plans', on_delete=models.CASCADE)