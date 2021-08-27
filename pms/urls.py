from pms.models import Notification
from django.urls import path
from . import views

urlpatterns = [
	path('', views.IndexView, name = "index"),
	path('home/', views.HomeView, name = "home"),
	path('createproject/', views.CreateProjectView, name = "createproject"),
	path('projects/', views.ProjectsView, name = "projects"),
	path('projects/<int:projectid>/', views.ProjectDetailsView, name = "projectdetails"),
	path('projects/addnewlevel/<int:projectid>/', views.AddNewLevelView, name = "addnewlevel"),
	path('projects/moveproject/<int:projectid>/<int:levelid>/', views.MoveProjectView, name = "moveproject"),
	path('projects/changedetails/<int:projectid>/', views.ChangeProjectDetailsView, name = "changedetails"),
	path('projects/addworker/<int:projectid>/<int:workerid>/', views.AddWorkersView, name = "addworker"),
	path('projects/relieveworker/<int:projectid>/<int:workerid>/', views.RelieveFromProjectView, name = "relieveworker"),
	path('notifications/', views.NotificationsView, name = "notifications"),
	path('notifications/markasread/<int:notificationid>/', views.NotificationMarkAsReadView, name = "markasread"),


	# AUTHENTICATION
	path('login/', views.LoginView, name = "login"),
	path('logout/', views.LogoutView, name = "logout"),
	path('register/', views.RegisterView, name = "register"),
]
