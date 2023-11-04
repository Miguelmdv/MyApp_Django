from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404
from .forms import CreateNewTask, CreateNewProject, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


# Create your views here.
def hello(request, username):
    return HttpResponse(f"<h1>Hello {username}</h1>")


def index(request):
    title = "Django practice!!"
    return render(request, "index.html", {"title": title})


def about(request):
    username = "Miguel Angel Madrid"
    return render(request, "about.html", {"username": username})


def projects(request):
    # projects = list(Project.objects.values())
    projects = Project.objects.all()
    return render(request, "projects/projects.html", {"projects": projects})


def tasks(request):
    tasks = Task.objects.all()
    return render(request, "tasks/tasks.html", {"tasks": tasks})


def create_project(request):
    if request.method == "GET":
        # show interface
        return render(
            request, "projects/create_project.html", {"form": CreateNewProject()}
        )
    else:
        # Save data
        Project.objects.create(name=request.POST["name"])
        return redirect("projects")


def create_task(request):
    if request.method == "GET":
        # show interface
        return render(request, "tasks/create_task.html", {"form": CreateNewTask()})
    else:
        # Save data
        Task.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            project_id=request.POST["project"],
        )
        return redirect("tasks")


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project=id)
    return render(request, "projects/detail.html", {"project": project, "tasks": tasks})


def delete_project(request):
    if request.method == "POST":
        if "project_id" in request.POST:
            project_id = request.POST["project_id"]
            if project_id:
                project = Project.objects.get(id=project_id)
                project.delete()

    previous_url = request.META.get("HTTP_REFERER", "projects")
    return redirect(previous_url)


def update_delete_task(request):
    if request.method == "POST":
        if "check_task" in request.POST:
            task_id = request.POST["check_task"]
            task = Task.objects.get(id=task_id)
            task.done = not task.done
            task.save()
        elif "task_id" in request.POST:
            task_id = request.POST["task_id"]
            if task_id:
                task = Task.objects.get(id=task_id)
                task.delete()

    previous_url = request.META.get("HTTP_REFERER", "tasks")
    return redirect(previous_url)


def signup(request):
    context = {"form": UserCreationForm(), "error_message": ""}
    if request.method == "POST":
        form = request.POST
        if form["password1"] == form["password2"]:
            try:
                user = User.objects.create_user(
                    form["username"], password=form["password1"]
                )
                user.save()
                login(request, user)
                return redirect("projects")
            except IntegrityError:
                context["error_message"] = "Username already exists"
                return render(request, "sign/signup.html", context)
        else:
            context["error_message"] = "Passwords don't match"
            return render(request, "sign/signup.html", context)
    else:
        return render(request, "sign/signup.html", context)


def signout(request):
    logout(request)
    return redirect("index")


def signin(request):
    context = {"form": AuthenticationForm(), "error_message": ""}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            context["error_message"] = "User or password is incorrect"
            return render(request, "sign/login.html", context)
        else:
            login(request, user)
            return redirect("projects")
    else:
        return render(request, "sign/login.html", context)
