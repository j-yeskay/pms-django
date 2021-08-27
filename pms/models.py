from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.db.models.deletion import PROTECT


class User(AbstractUser):
	company = models.CharField(max_length = 255, null = False, blank = False)


class Project(models.Model):
	owner = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE, related_name = "owner")
	name = models.CharField(max_length = 255, null = False, blank = False)
	description = models.CharField(max_length = 255, null = False, blank = False)
	workers = models.ManyToManyField(User, blank = True)
	all_status = models.ManyToManyField("ProjectLevel", blank = True)
	current_status = models.ForeignKey("ProjectLevel", on_delete = models.CASCADE, blank = True, null = True, related_name = "status")
	date_started = models.DateTimeField(auto_now_add = True)

	
	def __str__(self):
		return str(self.name + " by " + self.owner.username)


class ProjectLevel(models.Model):
	level_tag = models.CharField(max_length = 255)


	def __str__(self):
		return str(self.level_tag)


class Notification(models.Model):
	recipient = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE)
	content = models.CharField(max_length = 255, null = False, blank = False)
	read = models.BooleanField(default = False)
	date_created = models.DateTimeField(auto_now_add = True)


	class Meta:
		ordering = ['-date_created']

	
	def __str__(self):
		return str(self.content)



	

