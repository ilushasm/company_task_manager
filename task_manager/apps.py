from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_manager"

    def ready(self):
        from .utils import create_groups_and_permissions
        create_groups_and_permissions()
