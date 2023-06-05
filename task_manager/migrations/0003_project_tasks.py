# Generated by Django 4.2.1 on 2023-05-29 21:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0002_alter_project_options_alter_team_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="tasks",
            field=models.ManyToManyField(
                blank=True, related_name="tasks", to="task_manager.task"
            ),
        ),
    ]
