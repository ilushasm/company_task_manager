from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic


from task_manager.forms import WorkerCreationForm, TaskForm
from task_manager.models import Position, Worker, TaskType, Task, Team, Project


def index(request) -> HttpResponse:
    return render(request, "task_manager/index.html")


class PositionCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Position
    permission_required = "task_manager.add_position"

    fields = "__all__"
    template_name = "task_manager/position_form.html"
    success_url = reverse_lazy("task_manager:index")


class WorkerCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Worker
    permission_required = "task_manager.add_worker"
    form_class = WorkerCreationForm


class WorkerListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Worker
    permission_required = "task_manager.view_worker"
    paginate_by = 5
    queryset = Worker.objects.select_related("position").order_by("username")

    def get_queryset(self) -> QuerySet:
        queryset = get_user_model().objects.none()
        if self.request.user.groups.filter(name="Team Lead Group"):
            queryset = get_user_model().objects.all()
        elif self.request.user.groups.filter(name="Basic Group"):
            user_id = self.request.user.id
            team_id = Worker.objects.get(id=user_id).teammates.all()[0].id
            queryset = Worker.objects.prefetch_related(
                "teammates"
            ).filter(teammates=team_id).order_by("username")
        return queryset


class WorkerDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Worker
    permission_required = "task_manager.view_worker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(assignees__id=self.object.id)
        sort_by = self.request.GET.get("sort_by")
        context["tasks"] = Task.sorting(tasks, sort_by)

        return context


class TaskTypeCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = TaskType
    permission_required = "task_manager.add_tasktype"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class TaskCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    permission_required = "task_manager.add_task"

    def get_success_url(self) -> str:
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


class TeamCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Team
    permission_required = "task_manager.add_team"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class TeamListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5
    permission_required = "task_manager.view_team"
    queryset = Team.objects.all().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = 0
        if self.request.user.groups.filter(name="Basic Group"):
            user_id = self.request.user.id
            team_id = Worker.objects.get(id=user_id).teammates.all()[0].id
        context["team_id"] = team_id

        return context


class TeamDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Team
    permission_required = "task_manager.view_team"


class ProjectCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Project
    permission_required = "task_manager.add_project"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:index")


class ProjectListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Project
    ordering = ["name"]
    paginate_by = 5
    permission_required = "task_manager.view_project"


class ProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Project
    permission_required = "task_manager.view_project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.all()
        sort_by = self.request.GET.get("sort_by")

        context["tasks"] = Task.sorting(tasks, sort_by)

        return context


def custom_permission_denied(request, *args, **kwargs) -> HttpResponse:
    return render(request, "403.html", status=403)
