from django.contrib import admin
from . models import Notification, ProjectLevel, User, Project

admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectLevel)
admin.site.register(Notification)


