from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	company = models.CharField(max_length = 255, null = False, blank = False)


class Project(models.Model):
	owner = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE, related_name = "owner")
	name = models.CharField(max_length = 255, null = False, blank = False)
	description = models.CharField(max_length = 255, null = False, blank = False)
	workers = models.ManyToManyField(User, blank = True)
	date_started = models.DateTimeField(auto_now_add = True)

	
	def __str__(self):
		return str(self.name + " by " + self.owner.username)


class Notification(models.Model):
	recipient = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE)
	content = models.CharField(max_length = 255, null = False, blank = False)
	read = models.BooleanField(default = False)
	date_created = models.DateTimeField(auto_now_add = True)


	class Meta:
		ordering = ['-date_created']

	
	def __str__(self):
		return str(self.content)



	

