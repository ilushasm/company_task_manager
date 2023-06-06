from django.forms import forms


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
