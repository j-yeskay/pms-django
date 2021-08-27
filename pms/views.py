from pms.forms import UserRegistrationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Notification, Project, ProjectLevel, User
from . utils import get_project_owner_id_username, worker_already_in_project, get_no_of_notifications, get_no_of_projects


def IndexView(request):
	if request.user.is_authenticated:
		return redirect("home")
	else:
		return render(request, 'pms/index.html')


@login_required(login_url='index')
def HomeView(request):
	no_of_project_involved = sum(get_no_of_projects(request))
	return render(request, 'pms/home.html', {'n_p_i': no_of_project_involved, 'number_of_notifications': get_no_of_notifications(request)})


@login_required(login_url='index')
def CreateProjectView(request):
	if request.method == "POST":
		owner = request.user
		name = request.POST['name']
		description = request.POST['description']
		p = Project.objects.create(owner = owner, name = name, description = description)
		pl = ProjectLevel.objects.create(level_tag = "Created")
		p.all_status.add(pl)
		p.current_status = pl
		p.save()
		messages.success(request, "Project Created Successfully!")
		return redirect('projectdetails', projectid = p.pk)

	return render(request, 'pms/createproject.html', {'number_of_notifications': get_no_of_notifications(request)})


@login_required(login_url='index')
def ProjectsView(request):
	projects_as_owner = Project.objects.filter(owner = request.user)
	projects_as_worker = Project.objects.filter(workers__id = request.user.id)
	number_of_projects_as_owner, number_of_projects_as_worker = get_no_of_projects(request)
	return render(request, 'pms/projects.html', {'number_of_projects_as_owner': number_of_projects_as_owner, 'number_of_projects_as_worker': number_of_projects_as_worker,'projects_as_owner': projects_as_owner, 'projects_as_worker': projects_as_worker, 'number_of_notifications': get_no_of_notifications(request)})


@login_required(login_url='index')
def ProjectDetailsView(request, projectid):
	project_workers = Project.objects.get(id = projectid).workers.all()
	project = Project.objects.filter(id = projectid)
	project_statuses = Project.objects.get(id = projectid).all_status.all()
	if request.user.id ==  project[0].owner.id:
		user_is_project_owner = 1
		exclude_this = [request.user.id, project[0].owner.id]
		all_workers = User.objects.exclude(id__in = exclude_this)
		
		workers_from_same_company = all_workers.filter(company = request.user.company)
		workers_from_different_company = all_workers.exclude(company = request.user.company)

		workers_from_same_company = workers_from_same_company.difference(project_workers)
		workers_from_different_company = workers_from_different_company.difference(project_workers)
		
		no_of_project_workers = len(project_workers)
		no_of_workers_from_same_company = len(workers_from_same_company)
		no_of_workers_from_different_company = len(workers_from_different_company)
		
		return render(request, 'pms/projectdetails.html', {'project': project,'project_workers': project_workers, 'project_statuses': project_statuses, 'user_is_project_owner': user_is_project_owner,
							'workers_from_same_company': workers_from_same_company, 'workers_from_different_company': workers_from_different_company, 
							'n_p_w': no_of_project_workers,'n_w_s_c': no_of_workers_from_same_company, 'n_w_d_c': no_of_workers_from_different_company,
							'number_of_notifications': get_no_of_notifications(request)})
	else:
		user_is_project_owner = 0
		no_of_project_workers = len(project_workers)
		return render(request, 'pms/projectdetails.html', {'project': project,'project_workers': project_workers, 'user_is_project_owner': user_is_project_owner, 'n_p_w': no_of_project_workers, 'number_of_notifications': get_no_of_notifications(request)})


@login_required(login_url='index')
def AddNewLevelView(request, projectid):
	if request.method == "POST":
		p = Project.objects.get(id = projectid)
		pl = ProjectLevel.objects.create(level_tag = request.POST["leveltag"])
		p.all_status.add(pl)
		p.save()
		return redirect("projectdetails", projectid=projectid)



@login_required(login_url='index')
def MoveProjectView(request, projectid, levelid):
	p = Project.objects.get(id = projectid)
	l = ProjectLevel.objects.get(id = levelid)
	p.current_status = l
	p.save()
	return redirect("projectdetails", projectid=projectid)


@login_required(login_url='index')
def ChangeProjectDetailsView(request, projectid):
	project_owner_id , project_owner_username = get_project_owner_id_username(projectid)
	if request.user.id == project_owner_id:
		project = Project.objects.get(id = projectid)
		if request.method == "POST":
			project.name = request.POST['name']
			project.description = request.POST['description']
			project.save()
			return redirect("projectdetails", projectid=projectid)
		else:
			return render(request, 'pms/changeprojectdetails.html', {'projectid': projectid, 'name': project.name, 'description': project.description, 'number_of_notifications': get_no_of_notifications(request)})
	else:
		return redirect("projectdetails", projectid=projectid)



@login_required(login_url='index')
def AddWorkersView(request, projectid, workerid):
	project_owner_id , project_owner_username = get_project_owner_id_username(projectid)
	if (request.user.id ==  project_owner_id) and (request.user.id != workerid):
		worker = User.objects.get(id = workerid)
		project = Project.objects.get(id = projectid)
		if not worker_already_in_project(project, worker):
			project.workers.add(worker)
			Notification.objects.create(recipient = worker, content = str(project_owner_username) + " added you in a project.")
			messages.success(request, str(worker.username) + " added to project!")
	return redirect('projectdetails', projectid = projectid)


@login_required(login_url='index')
def RelieveFromProjectView(request, projectid, workerid):
	project_owner_id , project_owner_username = get_project_owner_id_username(projectid)
	if request.user.id ==  project_owner_id:
		project = Project.objects.get(id = projectid)
		worker = project.workers.get(id = workerid)
		project.workers.remove(worker)
		Notification.objects.create(recipient = worker, content = str(project_owner_username) + " relieved you from a project")
		messages.error(request, str(worker.username) + " relieved from project!")
	return redirect('projectdetails', projectid = projectid)


@login_required(login_url='index')
def NotificationsView(request):
	all_notifications = Notification.objects.filter(recipient = request.user)
	read_notifications = all_notifications.filter(read = True)
	unread_notifications = all_notifications.filter(read = False)
	return render(request, 'pms/notifications.html', {'read_notifications': read_notifications, 'unread_notifications': unread_notifications, 'number_of_notifications': get_no_of_notifications(request)})


@login_required(login_url="index")
def NotificationMarkAsReadView(request, notificationid):
	notification = Notification.objects.get(id = notificationid)
	if request.user == notification.recipient:
		notification.read = True
		notification.save()
		messages.warning(request, "Marked as Read!")
		return redirect('notifications')



# AUTHENTICATION

def LoginView(request):
	if request.user.is_authenticated:
		return redirect("home")
	
	else:
		if request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")

			user = authenticate(request, username = username, password = password)

			if user is not None:
				login(request, user)
				return redirect("home")
			else:
				messages.error(request, "Username or Password is WRONG!")
				return redirect("login")
	
	return render(request, 'pms/login.html')


def LogoutView(request):
	logout(request)
	return redirect("login")


def RegisterView(request):
	if request.user.is_authenticated:
		logout(request)
		
	form = UserRegistrationForm()
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account Created Successfully! Login Now!')
			return redirect("login")
	
	return render(request, 'pms/register.html', {'form':form})

