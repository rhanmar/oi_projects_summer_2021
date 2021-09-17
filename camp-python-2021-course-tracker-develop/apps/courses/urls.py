from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),
    path(
        "courses/<int:pk>/plan-schedule/",
        views.AutoPlanningView.as_view(),
        name="planning_form"
    ),
    path(
        "topic/<int:pk>/",
        views.TopicView.as_view(),
        name="topic-detail"
    ),
    path(
        "topic/become-speaker/",
        views.BecomeSpeakerView.as_view(),
        name="topic_become_speaker"
    ),
    path(
        "topic/reschedule/",
        views.RescheduleTopicView.as_view(),
        name="topic_reschedule"
    ),
    path(
        "task/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail"
    ),
    path("mytasks/", views.MyTasksView.as_view(), name="mytasks"),
    path(
        "solution/<int:pk>/",
        views.SolutionDetailView.as_view(),
        name="solution",
    ),
    path(
        "evaluations/delete/<int:pk>/",
        views.DeleteEvaluateView.as_view(),
        name="delete_solution",
    ),
    path(
        "evaluations/update/<int:pk>",
        views.EvaluationUpdateForm.as_view(),
        name="update_evaluation",
    )
]
