from .models import Notification, Project

def get_project_owner_id_username(projectid):
	project = Project.objects.filter(id = projectid)
	project_owner_id = project[0].owner.id
	project_owner_username = project[0].owner.username
	return project_owner_id, project_owner_username


def worker_already_in_project(project, worker):
	if len(project.workers.filter(id = worker.id)) == 0:
		return False 
	else:
		return True


def get_no_of_notifications(request):
	notifications = Notification.objects.filter(recipient = request.user)
	notifications = notifications.filter(read = False)
	return len(notifications)


def get_no_of_projects(request):
	projects_as_owner = Project.objects.filter(owner = request.user)
	projects_as_worker = Project.objects.filter(workers__id = request.user.id)
	return len(projects_as_owner), len(projects_as_worker)




