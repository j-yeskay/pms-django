from django.contrib import admin
from . models import Notification, User, Project

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Notification)


