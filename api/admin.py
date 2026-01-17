from django.contrib import admin

# Register your models here.
from .models import Tasks, Projects, Plans
admin.site.register(Tasks)
admin.site.register(Projects)
admin.site.register(Plans)