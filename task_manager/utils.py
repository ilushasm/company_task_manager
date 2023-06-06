from django.contrib.auth.models import Group, Permission
from django.forms import forms


def create_groups_and_permissions() -> None:
    # Creates Basic Group
    basic_group, _ = Group.objects.get_or_create(name="Basic Group")

    # Creates Team Lead Group
    team_lead_group, _ = Group.objects.get_or_create(name="Team Lead Group")

    # Assign permissions to Basic Group
    basic_permissions = Permission.objects.filter(
        content_type__app_label="task_manager",
        codename__in=[
            "view_task",
            "add_task",
            "change_task",
            "delete_task",
            "add_tasktype",
            "change_tasktype",
            "delete_tasktype",
            "view_tasktype",
            "view_worker",
            "view_project",
            "view_team",
        ],
    )
    basic_group.permissions.set(basic_permissions)

    # Assign permissions to Team Lead Group
    team_lead_permissions = Permission.objects.filter(
        content_type__app_label="task_manager",
        codename__in=[
            "add_project",
            "change_project",
            "delete_project",
            "view_project",
            "add_task",
            "change_task",
            "delete_task",
            "view_task",
            "add_tasktype",
            "change_tasktype",
            "delete_tasktype",
            "view_tasktype",
            "add_position",
            "change_position",
            "delete_position",
            "view_position",
            "add_team",
            "change_team",
            "delete_team",
            "view_team",
            "add_worker",
            "change_worker",
            "delete_worker",
            "view_worker",
        ],
    )
    team_lead_group.permissions.set(team_lead_permissions)


def get_team_form(form) -> forms.Form:
    form.fields["name"].widget.attrs["class"] = "form-control form-group"
    form.fields["team_lead"].widget.attrs["class"] = "form-control"
    form.fields["members"].widget.attrs["class"] = "form-check-input"
    form.fields["members"].widget.attrs["type"] = "checkbox"
    return form


def get_project_form(form) -> forms.Form:
    form.fields["name"].widget.attrs["class"] = "form-control form-group"
    form.fields["description"].widget.attrs["class"] = "form-control"
    form.fields["teams"].widget.attrs["class"] = "form-check-input"
    form.fields["teams"].widget.attrs["type"] = "checkbox"
    return form


def get_worker_form(form) -> forms.Form:
    form.fields["username"].widget.attrs["class"] = "form-control"
    form.fields["first_name"].widget.attrs["class"] = "form-control"
    form.fields["last_name"].widget.attrs["class"] = "form-control"
    form.fields["position"].widget.attrs["class"] = "form-control"
    form.fields["groups"].widget.attrs["class"] = "form-check-input"
    form.fields["groups"].widget.attrs["type"] = "checkbox"
    if "password1" in form.fields:
        form.fields["gender"].widget.attrs["class"] = "form-control"
        form.fields["password1"].widget.attrs["class"] = "form-control"
        form.fields["password2"].widget.attrs["class"] = "form-control"

    return form


def get_task_form(form) -> forms.Form:
    form.fields["name"].widget.attrs["class"] = "form-control form-group"
    form.fields["description"].widget.attrs["class"] = "form-control"
    form.fields["priority"].widget.attrs["class"] = "form-control"
    form.fields["deadline"].widget.attrs["class"] = "form-control"
    form.fields["assignees"].widget.attrs["class"] = "form-check-input"
    form.fields["assignees"].widget.attrs["type"] = "checkbox"
    return form
