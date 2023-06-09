# Generated by Django 4.2.1 on 2023-06-06 18:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0011_alter_worker_groups"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="team",
            new_name="teams",
        ),
        migrations.AlterField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(
                related_name="teams", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
