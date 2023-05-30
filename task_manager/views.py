from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic


from task_manager.forms import WorkerCreationForm, TaskForm
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


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 5
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(assignees__id=self.object.id)
        sort_by = self.request.GET.get("sort_by")
        context["tasks"] = Task.sorting(tasks, sort_by)

        return context


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        project = Project.objects.get(id=self.kwargs["project_id"])

        return reverse("task_manager:project-detail", kwargs={"pk": project.pk})

    def get_initial(self):
        initial = super().get_initial()
        project = Project.objects.get(id=self.kwargs["project_id"])
        initial["project"] = project.id

        return initial

    def form_valid(self, form):
        form.instance.project = Project.objects.get(id=self.kwargs["project_id"])

        return super().form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.all()
        sort_by = self.request.GET.get("sort_by")

        context["tasks"] = Task.sorting(tasks, sort_by)

        return context
