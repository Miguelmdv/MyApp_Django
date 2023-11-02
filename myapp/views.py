from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404
from .forms import CreateNewTask, CreateNewProject


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
    # task = get_object_or_404(Task, id=id)
    # return HttpResponse(f"Tasks: {task.title}")
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
        Project.objects.create(
            name=request.POST["name"]
        )
        return redirect("/projects/")


def create_task(request):
    if request.method == "GET":
        # show interface
        return render(request, "tasks/create_task.html", {"form": CreateNewTask()})
    else:
        # Save data
        Task.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            project_id=1,
        )
        return redirect("/tasks/")
