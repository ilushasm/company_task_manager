import datetime
from typing import Any, Dict

from django.db.models import QuerySet
from django.forms import forms

from task_manager.models import Task


def get_form(form) -> forms.Form:
    if "name" in form.fields:
        form.fields["name"].widget.attrs["class"] = "form-control"

    if "description" in form.fields:
        form.fields["description"].widget.attrs["class"] = "form-control"

    if "team_lead" in form.fields:
        form.fields["team_lead"].widget.attrs["class"] = "form-control"
        form.fields["members"].widget.attrs["class"] = "form-check-input"
        form.fields["members"].widget.attrs["type"] = "checkbox"

    if "teams" in form.fields:
        form.fields["teams"].widget.attrs["class"] = "form-check-input"
        form.fields["teams"].widget.attrs["type"] = "checkbox"

    if "username" in form.fields:
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

    if "priority" in form.fields:
        form.fields["priority"].widget.attrs["class"] = "form-control"
        form.fields["deadline"].widget.attrs["class"] = "form-control"
        form.fields["assignees"].widget.attrs["class"] = "form-check-input"
        form.fields["assignees"].widget.attrs["type"] = "checkbox"

    return form


def get_context_data(
        request,
        context: Dict[str, Any],
        tasks: QuerySet
) -> Dict[str, Any]:
    task_sorting = Task.task_sorting(
        hide_completed=request.GET.get("hide_completed"),
        cookie_hide_completed=request.session.get("hide_completed"),
        sort_by=request.GET.get("sort_by"),
        tasks=tasks,
    )
    request.session["hide_completed"] = task_sorting[
        "cookie_hide_completed"

    ]

    context["now"] = datetime.date.today()
    context["tasks"] = task_sorting["sorted_tasks"]
    context["hide_completed"] = task_sorting["hide_completed"]

    return context
