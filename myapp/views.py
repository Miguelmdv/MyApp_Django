from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Project, Task
from django.shortcuts import get_object_or_404

# Create your views here.
def hello(request, username):
    return HttpResponse(f"<h1>Hello {username}</h1>")    

def index(request):
    title = "Django practice!!"
    return render(request, "index.html", {"title": title})

def about(request):
    username = "Miguel Angel Madrid"
    return render(request, "about.html", {"username":username})

def projects(request):
    # projects = list(Project.objects.values())
    projects = Project.objects.all()
    return render(request, "projects.html", {"projects": projects})

def tasks(request):
    # task = get_object_or_404(Task, id=id)
    # return HttpResponse(f"Tasks: {task.title}")
    tasks = Task.objects.all()
    return render(request, "tasks.html", {"tasks": tasks})