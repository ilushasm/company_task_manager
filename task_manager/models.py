from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, default=1)
    REQUIRED_FIELDS = ["position_id"]

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_absolute_url(self) -> str:
        return reverse("task_manager:worker-detail", args=[str(self.id)])


class Team(models.Model):
    team_lead = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=63)
    members = models.ManyToManyField(get_user_model(), related_name="teammates")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("task_manager:team-detail", args=[str(self.id)])


class Project(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    team = models.ManyToManyField(Team, related_name="projects", blank=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("task_manager:project-detail", args=[str(self.id)])

    def get_percentage(self) -> int:
        percentage = 0
        total_tasks = self.tasks.all()
        completed_tasks = total_tasks.filter(is_completed=True).count()
        if total_tasks.count() != 0 and completed_tasks != 0:
            percentage = (completed_tasks / total_tasks.count()) * 100

        return round(percentage)


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Normal", "Normal"),
        ("Low", "Low"),
    )

    name = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(get_user_model(), related_name="assigned", blank=True)

    @classmethod
    def sorting(cls, tasks, sort_by: str) -> object:
        if sort_by == "deadline":
            tasks = tasks.order_by("deadline", "is_completed")
        elif sort_by == "is_completed":
            tasks = tasks.order_by("deadline", "is_completed")
        elif sort_by == "priority":
            tasks = tasks.order_by(
                models.Case(
                    models.When(priority="Urgent", then=0),
                    models.When(priority="High", then=1),
                    models.When(priority="Normal", then=2),
                    models.When(priority="Low", then=3),
                    default=4,
                    output_field=models.IntegerField(),
                )
            )
        return tasks

    @staticmethod
    def task_sorting(hide_completed, cookie_hide_completed, tasks) -> dict:
        if hide_completed is None and cookie_hide_completed is not None:
            hide_completed = cookie_hide_completed
        elif hide_completed is not None and hide_completed != cookie_hide_completed:
            cookie_hide_completed = hide_completed

        if hide_completed == "True":
            tasks = tasks.filter(is_completed=False)

        return {
            "sorted_tasks": tasks,
            "hide_completed": hide_completed,
            "cookie_hide_completed": cookie_hide_completed
        }

    def __str__(self) -> str:
        return self.name
