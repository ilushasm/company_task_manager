from django.contrib.auth.models import Group, Permission


def create_groups_and_permissions() -> None:
    # Create Basic Group
    basic_group, _ = Group.objects.get_or_create(name="Basic Group")

    # Create Team Lead Group
    team_lead_group, _ = Group.objects.get_or_create(name="Team Lead Group")

    # Assign permissions to Basic Group
    basic_permissions = Permission.objects.filter(
        content_type__app_label="task_manager",
        codename__in=["change_project", "view_task",
                      "add_task", "change_task", "delete_task",
                      "add_tasktype", "change_tasktype", "delete_tasktype",
                      "view_tasktype", "view_worker", "view_project",
                      "view_team"
                      ]
    )
    basic_group.permissions.set(basic_permissions)

    # Assign permissions to Team Lead Group
    team_lead_permissions = Permission.objects.filter(
        content_type__app_label="task_manager",
        codename__in=["add_project", "change_project", "delete_project",
                      "view_project",
                      "add_task", "change_task", "delete_task",
                      "view_task",
                      "add_tasktype", "change_tasktype", "delete_tasktype",
                      "view_tasktype",
                      "add_position", "change_position", "delete_position",
                      "view_position",
                      "add_team", "change_team", "delete_team",
                      "change_team",
                      "add_worker", "change_worker", "delete_worker",
                      "view_worker"]
    )
    team_lead_group.permissions.set(team_lead_permissions)
