# Generated by Django 4.2.1 on 2023-06-03 03:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0009_alter_worker_groups"),
    ]

    operations = [
        migrations.AddField(
            model_name="worker",
            name="avatar",
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AddField(
            model_name="worker",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")], default="M", max_length=1
            ),
        ),
    ]