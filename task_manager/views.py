from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View

from task_manager.forms import WorkerCreationForm, TaskForm, TaskCreateForm
from task_manager.models import Position, Worker, TaskType, Task, Team, Project


def index(request) -> render:
    return render(request, "task_manager/index.html")


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "task_manager/position_form.html"
    success_url = reverse_lazy("task_manager:index")


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class TaskCreateView(View):
    # model = Task
    # form_class = TaskForm
    # success_url = reverse_lazy("task_manager:index")
    def get(self, request, project_id):
        form = TaskCreateForm(initial={"project": project_id})
        return render(request, "task_manager/task_form.html", {"form": form})

    def post(self, request, project_id):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "task_manager/index.html")
            # Redirect or do something else
        return render(request, "task_manager/task_form.html", {"form": form})


class TeamCreateView(generic.CreateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class TeamListView(generic.ListView):
    model = Team
    paginate_by = 5


class TeamDetailView(generic.DetailView):
    model = Team


class ProjectCreateView(generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 5


class ProjectDetailView(generic.DetailView):
    model = Project
