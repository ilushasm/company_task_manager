import datetime
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet, Count
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from task_manager import utils
from task_manager.forms import WorkerCreationForm, TaskForm, TeamFrom, ProjectForm
from task_manager.models import Position, Worker, TaskType, Task, Team, Project


def index(request) -> HttpResponse:
    return render(request, "task_manager/index.html")


class PositionCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Position
    permission_required = "task_manager.add_position"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class PositionUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    permission_required = "task_manager.change_position"
    success_url = reverse_lazy("task_manager:position-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class PositionDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = Position
    permission_required = "task_manager.delete_position"
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        workers = Worker.objects.filter(position=kwargs["object"])
        context["workers"] = workers
        return context


class PositionListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 20
    permission_required = "task_manager.view_position"
    queryset = Position.objects.all().order_by("name")

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        position_list = Position.objects.all().prefetch_related("worker_set").order_by("name")

        for position in position_list:
            position.count = Worker.objects.filter(position_id=position.id).count()

        context["position_list"] = position_list

        return context


class WorkerCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Worker
    permission_required = "task_manager.add_worker"
    form_class = WorkerCreationForm


class WorkerListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Worker
    permission_required = "task_manager.view_worker"
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        queryset = get_user_model().objects.none()
        if self.request.user.groups.filter(name="Team Lead Group"):
            queryset = get_user_model().objects.all().order_by("username")
        elif self.request.user.groups.filter(name="Basic Group"):
            user_id = self.request.user.id
            team_id = get_user_model().objects.get(id=user_id).teammates.all()[0].id
            queryset = get_user_model().objects.prefetch_related(
                "teammates"
            ).filter(teammates=team_id).order_by("username")
        return queryset


class WorkerDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Worker
    permission_required = "task_manager.view_worker"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(assignees__id=self.object.id)
        sort_by = self.request.GET.get("sort_by")
        context["tasks"] = Task.sorting(tasks, sort_by)

        return context


class WorkerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position"]
    permission_required = "task_manager.change_worker"

    def get_success_url(self) -> str:
        return reverse("task_manager:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = Worker
    permission_required = "task_manager.delete_worker"
    success_url = reverse_lazy("task_manager:worker-list")


class TaskTypeCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = TaskType
    permission_required = "task_manager.add_tasktype"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class TaskTypeUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    permission_required = "task_manager.change_tasktype"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class TaskTypeDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    permission_required = "task_manager.delete_tasktype"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(task_type=kwargs["object"])
        context["tasks"] = tasks
        return context


class TaskTypeListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = TaskType
    permission_required = "task_manager.view_tasktype"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        tasktype_list = TaskType.objects.all().prefetch_related("task_set").order_by("name")

        for tasktype in tasktype_list:
            tasktype.count = Task.objects.filter(task_type_id=tasktype.id).count()

        context["tasktype_list"] = tasktype_list

        return context


class TaskCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    permission_required = "task_manager.add_task"

    def get_success_url(self) -> str:
        project = Project.objects.get(id=self.kwargs["project_id"])

        return reverse("task_manager:project-detail", kwargs={"pk": project.pk})

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        project = Project.objects.get(id=self.kwargs["project_id"])
        initial["project"] = project.id

        return initial

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["project_id"] = self.kwargs["project_id"]
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        form.instance.project = Project.objects.get(id=self.kwargs["project_id"])

        return super().form_valid(form)


class TaskUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
    permission_required = "task_manager.change_task"

    def get_success_url(self) -> str:
        return reverse("task_manager:project-detail", kwargs={"pk": self.object.project.pk})


class TaskDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = Task
    permission_required = "task_manager.delete_task"

    def get_success_url(self) -> str:
        return reverse("task_manager:project-detail", kwargs={"pk": self.object.project.pk})


class TaskCompleteView(View):
    @staticmethod
    def post(request, pk) -> HttpResponseRedirect:
        task = Task.objects.get(pk=pk)
        task.is_completed = True
        task.save()
        return HttpResponseRedirect(reverse('task_manager:project-detail', args=[task.project.pk]))


class TeamCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamFrom
    permission_required = "task_manager.add_team"
    success_url = reverse_lazy("task_manager:team-list")

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_team_form(form)
        return form


class TeamListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5
    ordering = ["name"]
    permission_required = "task_manager.view_team"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        team_list = Team.objects.all().prefetch_related("projects").order_by("name")

        context["team_list"] = team_list

        return context


class TeamDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Team
    permission_required = "task_manager.view_team"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        members_list = kwargs["object"].members.annotate(task_count=Count("assigned"))

        context["members_list"] = members_list

        return context


class TeamUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamFrom
    permission_required = "task_manager.change_team"

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_team_form(form)
        return form

    def get_success_url(self) -> str:
        return reverse("task_manager:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")
    permission_required = "task_manager.delete_team"


class ProjectCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    permission_required = "task_manager.add_project"
    success_url = reverse_lazy("task_manager:project-list")

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_project_form(form)
        return form


class ProjectListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Project
    ordering = ["name"]
    paginate_by = 5
    permission_required = "task_manager.view_project"


class ProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Project
    permission_required = "task_manager.view_project"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tasks = self.object.tasks.all().order_by("deadline")

        sort_by = self.request.GET.get("sort_by")
        hide_completed = self.request.GET.get("hide_completed")
        cookie_hide_completed = self.request.session.get("hide_completed")

        if hide_completed is None and cookie_hide_completed is not None:
            hide_completed = cookie_hide_completed
        elif hide_completed is not None and hide_completed != cookie_hide_completed:
            self.request.session["hide_completed"] = hide_completed

        if hide_completed == "True":
            tasks = tasks.filter(is_completed=False)

        is_member = kwargs["object"].team.filter(members__id=self.request.user.id).exists()

        print(Task.objects.first().deadline)

        context["now"] = datetime.date.today()
        context["is_member"] = is_member
        context["tasks"] = Task.sorting(tasks, sort_by)
        context["hide_completed"] = hide_completed
        return context


class ProjectUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    permission_required = "task_manager.change_project"

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_project_form(form)
        return form

    def get_success_url(self) -> str:
        return reverse("task_manager:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = Project
    permission_required = "task_manager.delete_project"
    success_url = reverse_lazy("task_manager:project-list")


def custom_permission_denied(request, *args, **kwargs) -> HttpResponse:
    return render(request, "403.html", status=403)
