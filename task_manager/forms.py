from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from task_manager.models import Worker, TaskType, Task


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class DateInput(forms.DateInput):
    input_type = "date"


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees"
        ]
        widgets = {
            "deadline": DateInput(),
        }


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees",
            "project"
        ]
        widgets = {
            'project': forms.HiddenInput(),
            "deadline": DateInput(),
        }