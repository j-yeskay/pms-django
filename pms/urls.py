from django.urls import path
from . import views

urlpatterns = [
	path('', views.IndexView, name = "index"),
	path('home/', views.HomeView, name = "home"),
	path('createproject/', views.CreateProjectView, name = "createproject"),
	path('projects/', views.ProjectsView, name = "projects"),
	path('projects/<int:projectid>/', views.ProjectDetails, name = "projectdetails"),
	path('projects/addworker/<int:projectid>/<int:workerid>/', views.AddWorkersView, name = "addworker"),
	path('projects/relieveworker/<int:projectid>/<int:workerid>/', views.RelieveFromProjectView, name = "relieveworker"),


	# AUTHENTICATION
	path('login/', views.LoginView, name = "login"),
	path('logout/', views.LogoutView, name = "logout"),
	path('register/', views.RegisterView, name = "register"),
]
