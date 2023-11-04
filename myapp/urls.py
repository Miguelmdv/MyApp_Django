from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("hello/<str:username>", views.hello, name="hello"),
    path("projects/", views.projects, name="projects"),
    path("projects/<int:id>", views.project_detail, name="project_detail"),
    path("tasks/", views.tasks, name="tasks"),
    path("create_project/", views.create_project, name="create_project"),
    path("create_task/", views.create_task, name="create_task"),
    path("projects", views.delete_project, name="delete_project"),
    path("task", views.update_delete_task, name="update_delete_task"),
    path("signup/", views.signup, name="sign_up"),
    path("logout/", views.signout, name="log_out"),
    path("login/", views.signin, name="log_in"),
]
