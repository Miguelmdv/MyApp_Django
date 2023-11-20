from django.shortcuts import render, redirect
from .models import Project, Task
from django.shortcuts import get_object_or_404
from .forms import TaskForm, ProjectForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
import re


# My methods
def previous_url_without_num(p_url):
    pattern = r"\d+$"
    p_url_wn = re.sub(pattern, "", p_url)
    if p_url_wn != p_url:
        p_url = p_url_wn
    return p_url


# Create your views here.
def index(request):
    title = "Django practice!!"
    return render(request, "index.html", {"title": title})


def about(request):
    username = "Miguel Angel Madrid"
    return render(request, "about.html", {"username": username})


@login_required
def projects(request):
    if request.method == "GET":
        context = {"form": ProjectForm(), "projects": None, "error_message": ""}
        context["projects"] = Project.objects.filter(user=request.user)
        return render(request, "projects/projects.html", context)
    else:
        return redirect("projects")


@login_required
def tasks(request):
    tasks_all = Task.objects.filter(project__user=request.user)
    tasks_completed = Task.objects.filter(done=True, project__user=request.user)
    tasks_incompleted_notimportant = Task.objects.filter(
        done=False, important=False, project__user=request.user
    )
    tasks_incompleted_important = Task.objects.filter(
        done=False, important=True, project__user=request.user
    )
    tasks = {
        "tasks_all": tasks_all,
        "tasks_completed": tasks_completed,
        "tasks_incompleted_notimportant": tasks_incompleted_notimportant,
        "tasks_incompleted_important": tasks_incompleted_important,
    }
    return render(request, "tasks/tasks.html", {"tasks": tasks})


@login_required
def create_project(request):
    projects = Project.objects.filter(user=request.user)
    context = {"form": ProjectForm(), "projects": projects, "error_message": ""}
    if request.method == "POST":
        # Save data
        try:
            form = ProjectForm(request.POST)
            new_project = form.save(commit=False)
            new_project.user = request.user
            new_project.save()
        except ValueError:
            context["error_message"] = "Project is not valid"
    return render(request, "projects/projects.html", context)


@login_required
def create_task(request):
    projects_user = Project.objects.filter(user=request.user)
    form = TaskForm(projects_user=projects_user)
    context = {"form": form, "error_message": ""}

    if request.method == "GET":
        # show interface
        return render(request, "tasks/create_task.html", context)

    else:
        try:
            form = TaskForm(request.POST, projects_user=projects_user)

            if form.is_valid():
                form.save()

        except ValueError:
            context["error_message"] = "Could not create task"
            return render(request, "tasks/create_task.html", context)

        return redirect("tasks")


@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)

    tasks_all = Task.objects.filter(project=id)
    tasks_completed = Task.objects.filter(project=id, done=True)
    tasks_incompleted_notimportant = Task.objects.filter(
        project=id, done=False, important=False
    )
    tasks_incompleted_important = Task.objects.filter(
        project=id, done=False, important=True
    )
    tasks = {
        "tasks_all": tasks_all,
        "tasks_completed": tasks_completed,
        "tasks_incompleted_notimportant": tasks_incompleted_notimportant,
        "tasks_incompleted_important": tasks_incompleted_important,
    }
    return render(
        request, "projects/project_detail.html", {"project": project, "tasks": tasks}
    )


@login_required
def task_detail(request, id):
    task = get_object_or_404(Task, id=id, project__user=request.user)
    projects_user = Project.objects.filter(user=request.user)
    form = TaskForm(instance=task, projects_user=projects_user)
    return render(request, "tasks/task_detail.html", {"task": task, "form": form})


@login_required
def delete_project(request):
    if request.method == "POST":
        if "delete_project" in request.POST:
            project_id = request.POST["delete_project"]
            if project_id:
                project = get_object_or_404(Project, id=project_id)
                project.delete()

    previous_url = request.META.get("HTTP_REFERER", "projects")
    return redirect(previous_url)


@login_required
def update_delete_task(request):
    previous_url = request.META.get("HTTP_REFERER", "tasks")
    if request.method == "POST":
        if "check_task" in request.POST:
            task_id = request.POST["check_task"]
            if task_id:
                task = get_object_or_404(Task, id=task_id, project__user=request.user)
                task.done = not task.done
                if task.done:
                    task.datecompleted = timezone.now()
                else:
                    task.datecompleted = None
                task.save()

        elif "imp_task" in request.POST:
            try:
                task_id = request.POST["imp_task"]
                if task_id:
                    task = get_object_or_404(Task, id=task_id)
                    task.important = not task.important
                    task.save()
            except:
                print("Error al marcar como importante la tarea")

        elif "update_task" in request.POST:
            try:
                task_id = request.POST["update_task"]
                if task_id:
                    task = get_object_or_404(
                        Task, id=task_id, project__user=request.user
                    )
                    projects_user = Project.objects.filter(user=request.user)
                    form = TaskForm(
                        request.POST, instance=task, projects_user=projects_user
                    )
                    if form.is_valid():
                        form.save()
                        previous_url = previous_url_without_num(previous_url)
            except:
                print("Error al actualizar la tarea")

        elif "delete_task" in request.POST:
            try:
                task_id = request.POST["delete_task"]
                if task_id:
                    task = get_object_or_404(Task, id=task_id)
                    task.delete()
                    previous_url = previous_url_without_num(previous_url)
            except:
                print("Error al borrar la tarea")

    return redirect(previous_url)


def signup(request):
    context = {"form": CustomUserCreationForm(), "error_message": ""}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("projects")
        else:
            error_message = form
            context["form"] = form
            context["error_message"] = error_message
    else:
        form = CustomUserCreationForm()
    return render(request, "sign/signup.html", context)


@login_required
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
            if request.GET.get("next") == None:
                return redirect("projects")
            return redirect(f"{request.GET.get('next')}/")
    else:
        return render(request, "sign/login.html", context)


def tasks2(request):
    return render(request, "tasks/tasks2.html")
