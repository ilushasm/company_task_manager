from django.urls import path

from task_manager.views import (
    index,
    PositionCreateView,
    PositionListView,
    PositionDeleteView,
    PositionUpdateView,
    WorkerCreateView,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerDeleteView,
    WorkerChangePasswordView,
    TaskTypeCreateView,
    TaskTypeListView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskCompleteView,
    TeamCreateView,
    TeamDetailView,
    TeamListView,
    TeamUpdateView,
    TeamDeleteView,
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "position-create/",
        PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "position-list/",
        PositionListView.as_view(),
        name="position-list",
    ),
    path(
        "position-update/<int:pk>/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "position-delete/<int:pk>/",
        PositionDeleteView.as_view(),
        name="position-delete",
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
        "worker-update/<int:pk>/",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "worker-delete/<int:pk>/",
        WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path(
        "change-password/<int:pk>/",
        WorkerChangePasswordView.as_view(),
        name="change-password",
    ),
    path("tasktype-create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path(
        "tasktype-list/",
        TaskTypeListView.as_view(),
        name="task-type-list",
    ),
    path(
        "tasktype-update/<int:pk>/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "tasktype-delete/<int:pk>/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path("task-create/<int:project_id>/", TaskCreateView.as_view(), name="task-create"),
    path("task-update/<int:pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("task-delete/<int:pk>/", TaskDeleteView.as_view(), name="task-delete"),
    path("task-complete/<int:pk>/", TaskCompleteView.as_view(), name="task-complete"),
    path("team-create/", TeamCreateView.as_view(), name="team-create"),
    path("team-list/", TeamListView.as_view(), name="team-list"),
    path("team/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("team-update/<int:pk>/", TeamUpdateView.as_view(), name="team-update"),
    path("team-delete/<int:pk>/", TeamDeleteView.as_view(), name="team-delete"),
    path("project-create/", ProjectCreateView.as_view(), name="project-create"),
    path("project-list/", ProjectListView.as_view(), name="project-list"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path(
        "project-update/<int:pk>/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "project-delete/<int:pk>/", ProjectDeleteView.as_view(), name="project-delete"
    ),
]

app_name = "task_manager"
