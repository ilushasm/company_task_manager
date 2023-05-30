from django.urls import path, include

from task_manager.views import (
    index,
    PositionCreateView,
    WorkerCreateView,
    WorkerListView,
    WorkerDetailView,
    TaskTypeCreateView,
    TaskCreateView,
    TeamCreateView,
    TeamDetailView,
    TeamListView,
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "position-create/",
        PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "worker-create/",
        WorkerCreateView.as_view(),
        name="worker-create",
    ),
    path(
        "worker-list/",
        WorkerListView.as_view(),
        name="worker-list",
    ),
    path(
        "worker/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail",
    ),
    path(
        "tasktype-create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task-create/<int:project_id>/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "team-create/",
        TeamCreateView.as_view(),
        name="team-create"
    ),
    path(
        "team-list/",
        TeamListView.as_view(),
        name="team-list"
    ),
    path(
        "team/<int:pk>/",
        TeamDetailView.as_view(),
        name="team-detail"
    ),
    path(
        "project-create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path(
        "project-list/",
        ProjectListView.as_view(),
        name="project-list"
    ),
    path(
        "project/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail"
    )
]

app_name = "task_manager"
