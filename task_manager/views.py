import datetime
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Count
from django.forms import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from task_manager import utils
from task_manager.forms import (
    WorkerCreationForm,
    TaskForm,
    TeamFrom,
    ProjectForm,
    WorkerUpdateForm,
)
from task_manager.models import Position, Worker, TaskType, Task, Team, Project


def index(request) -> HttpResponse:
    tasks = Task.objects.all().count()
    projects = Project.objects.all().count()
    teams = Team.objects.all().count()
    workers = get_user_model().objects.all().count()
    context = {"tasks": tasks, "projects": projects, "teams": teams, "workers": workers}

    return render(request, "task_manager/index.html", context)


class PositionCreateView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView
):
    model = Position
    permission_required = "task_manager.add_position"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class PositionUpdateView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView
):
    model = Position
    fields = "__all__"
    permission_required = "task_manager.change_position"
    success_url = reverse_lazy("task_manager:position-list")

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class PositionDeleteView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView
):
    model = Position
    permission_required = "task_manager.delete_position"
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        workers = Worker.objects.filter(position=kwargs["object"])
        context["workers"] = workers
        return context


class PositionListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Position
    permission_required = "task_manager.view_position"
    queryset = Position.objects.all().order_by("name")


class WorkerCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    permission_required = "task_manager.add_worker"

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_worker_form(form)
        return form


class WorkerListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    permission_required = "task_manager.view_worker"


class WorkerDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Worker
    permission_required = "task_manager.view_worker"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(assignees__id=self.object.id).order_by("name")
        sort_by = self.request.GET.get("sort_by")

        task_sorting = Task.task_sorting(
            hide_completed=self.request.GET.get("hide_completed"),
            cookie_hide_completed=self.request.session.get("hide_completed"),
            tasks=tasks,
        )
        self.request.session["hide_completed"] = task_sorting["cookie_hide_completed"]

        context["now"] = datetime.date.today()
        context["tasks"] = Task.sorting(task_sorting["sorted_tasks"], sort_by)
        context["hide_completed"] = task_sorting["hide_completed"]

        return context


class WorkerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    permission_required = "task_manager.change_worker"

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_worker_form(form)
        return form


class WorkerDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = Worker
    permission_required = "task_manager.delete_worker"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerChangePasswordView(PasswordChangeView):
    template_name = "task_manager/change_password.html"

    def get_success_url(self) -> str:
        return reverse("task_manager:worker-detail", kwargs={"pk": self.kwargs["pk"]})


class TaskTypeCreateView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView
):
    model = TaskType
    permission_required = "task_manager.add_tasktype"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class TaskTypeUpdateView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView
):
    model = TaskType
    fields = "__all__"
    permission_required = "task_manager.change_tasktype"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs["class"] = "form-control"
        return form


class TaskTypeDeleteView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView
):
    model = TaskType
    permission_required = "task_manager.delete_tasktype"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(task_type=kwargs["object"])
        context["tasks"] = tasks
        return context


class TaskTypeListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = TaskType
    permission_required = "task_manager.view_tasktype"


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

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_task_form(form)
        return form

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["project_id"] = self.kwargs["project_id"]
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        form.instance.project = Project.objects.get(id=self.kwargs["project_id"])

        return super().form_valid(form)


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_task_form(form)
        return form

    def get_success_url(self) -> str:
        return reverse(
            "task_manager:project-detail", kwargs={"pk": self.object.project.pk}
        )

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["project_id"] = self.object.project.id
        return kwargs


class TaskDeleteView(PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView):
    model = Task
    permission_required = "task_manager.delete_task"

    def get_success_url(self) -> str:
        return reverse(
            "task_manager:project-detail", kwargs={"pk": self.object.project.pk}
        )


class TaskCompleteView(View):
    @staticmethod
    def post(request, pk) -> HttpResponseRedirect:
        task = Task.objects.get(pk=pk)
        task.is_completed = True
        task.save()
        return HttpResponseRedirect(
            reverse("task_manager:project-detail", args=[task.project.pk])
        )


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
    queryset = Team.objects.all().prefetch_related("projects").order_by("name")
    permission_required = "task_manager.view_team"


class TeamDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    model = Team
    permission_required = "task_manager.view_team"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
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


class ProjectCreateView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView
):
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
    permission_required = "task_manager.view_project"


class ProjectDetailView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView
):
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

        is_member = (
            kwargs["object"].teams.filter(members__id=self.request.user.id).exists()
        )

        context["now"] = datetime.date.today()
        context["is_member"] = is_member
        context["tasks"] = Task.sorting(tasks, sort_by)
        context["hide_completed"] = hide_completed
        return context


class ProjectUpdateView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView
):
    model = Project
    form_class = ProjectForm
    permission_required = "task_manager.change_project"

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form = utils.get_project_form(form)
        return form

    def get_success_url(self) -> str:
        return reverse("task_manager:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(
    PermissionRequiredMixin, LoginRequiredMixin, generic.DeleteView
):
    model = Project
    permission_required = "task_manager.delete_project"
    success_url = reverse_lazy("task_manager:project-list")


def custom_permission_denied(request, *args, **kwargs) -> HttpResponse:
    return render(request, "403.html", status=403)
