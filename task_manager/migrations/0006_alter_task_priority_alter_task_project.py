# Generated by Django 4.2.1 on 2023-05-30 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0005_alter_task_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[
                    ("Urgent", "Urgent"),
                    ("High", "High"),
                    ("Normal", "Normal"),
                    ("Low", "Low"),
                ],
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="task_manager.project",
            ),
        ),
    ]
