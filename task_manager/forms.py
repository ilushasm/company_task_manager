from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from task_manager.models import Worker, Task, Team, Project


class WorkerCreationForm(UserCreationForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
            "groups"
        )

    def save(self, commit=True) -> Worker:
        worker = super().save(commit=False)
        if commit:
            worker.save()

        return worker


class DateInput(forms.DateInput):
    input_type = "date"


class TaskForm(forms.ModelForm):
    def __init__(self, project_id, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        id_list = Team.objects.filter(
            projects__id=project_id
        ).values_list('members', flat=True)
        queryset_two = get_user_model().objects.filter(id__in=list(id_list))
        self.fields['assignees'].queryset = queryset_two

    class Meta:
        model = Task
        fields = ["name", "description", "priority", "deadline", "task_type", "is_completed", "assignees"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "task_type": forms.Select(attrs={"class": "form-control"}),
            "is_completed": forms.CheckboxInput(),
            "assignees": forms.CheckboxSelectMultiple()
        }


class TeamFrom(forms.ModelForm):

    class Meta:
        model = Team
        fields = ["name", "team_lead", "members"]
        widgets = {
            "members": forms.CheckboxSelectMultiple(),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["name", "description", "team"]
        widgets = {
            "team": forms.CheckboxSelectMultiple(),
        }

