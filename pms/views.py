from pms.forms import UserRegistrationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Project, User

def IndexView(request):
	if request.user.is_authenticated:
		return redirect("home")
	else:
		return render(request, 'pms/index.html')


@login_required(login_url='index')
def HomeView(request):
	projects_as_owner = Project.objects.filter(owner = request.user)
	projects_as_worker = Project.objects.filter(workers__id = request.user.id)
	no_of_projects_involved = len(projects_as_owner) + len(projects_as_worker)
	return render(request, 'pms/home.html', {'n_p_i': no_of_projects_involved})


@login_required(login_url='index')
def CreateProjectView(request):
	if request.method == "POST":
		owner = request.user
		name = request.POST['name']
		description = request.POST['description']
		Project.objects.create(owner = owner, name = name, description = description)
		return redirect('home')



	return render(request, 'pms/createproject.html')


@login_required(login_url='index')
def ProjectsView(request):
	projects_as_owner = Project.objects.filter(owner = request.user)
	projects_as_worker = Project.objects.filter(workers__id = request.user.id)
	return render(request, 'pms/projects.html', {'projects_as_owner': projects_as_owner, 'projects_as_worker': projects_as_worker})


@login_required(login_url='index')
def ProjectDetails(request, projectid):
	project_workers = Project.objects.get(id = projectid).workers.all()
	project = Project.objects.filter(id = projectid)

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
		
		return render(request, 'pms/projectdetails.html', {'project': project,'project_workers': project_workers,'user_is_project_owner': user_is_project_owner,
							'workers_from_same_company': workers_from_same_company, 'workers_from_different_company': workers_from_different_company, 
							'n_p_w': no_of_project_workers,'n_w_s_c': no_of_workers_from_same_company, 'n_w_d_c': no_of_workers_from_different_company})
	else:
		user_is_project_owner = 0
		no_of_project_workers = len(project_workers)
		return render(request, 'pms/projectdetails.html', {'project': project,'project_workers': project_workers, 'user_is_project_owner': user_is_project_owner, 'n_p_w': no_of_project_workers})

@login_required(login_url='index')
def AddWorkersView(request, projectid, workerid):
	project = Project.objects.filter(id = projectid)
	if request.user.id ==  project[0].owner.id:
		worker = User.objects.get(id = workerid)
		project = Project.objects.get(id = projectid)
		project.workers.add(worker)
	return redirect('projectdetails', projectid = projectid)


@login_required(login_url='index')
def RelieveFromProjectView(request, projectid, workerid):
	project = Project.objects.filter(id = projectid)
	if request.user.id ==  project[0].owner.id:
		project = Project.objects.get(id = projectid)
		worker = project.workers.get(id = workerid)
		project.workers.remove(worker)
	return redirect('projectdetails', projectid = projectid)





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

