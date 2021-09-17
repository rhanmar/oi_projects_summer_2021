from django.urls import path

from . import views

app_name = "startups"
urlpatterns = [
    path(
        "",
        views.startups.StartupsListView.as_view(),
        name="startups_list",
    ),
    path(
        "<int:pk>/",
        views.startups.StartupsDetailView.as_view(),
        name="startup_detail",
    ),
    path(
        "vacancies/",
        views.vacancies.VacanciesListView.as_view(),
        name="vacancies_list",
    ),
    path(
        "vacancies/<int:pk>",
        views.vacancies.VacancyDetailView.as_view(),
        name="vacancy_detail",
    ),
    path(
        "create",
        views.startups.StartupCreateView.as_view(),
        name="startup_create",
    ),
    path(
        "<int:pk>/update",
        views.startups.StartupUpdateView.as_view(),
        name="startup_update",
    ),
    path(
        "<int:pk>/delete",
        views.startups.StartupDeleteView.as_view(),
        name="startup_delete",
    ),
    path(
        "vacancies/<int:pk>/update",
        views.vacancies.VacancyUpdateView.as_view(),
        name="vacancy_update",
    ),
    path(
        "vacancies/<int:pk>/delete",
        views.vacancies.VacancyDeleteView.as_view(),
        name="vacancy_delete",
    ),
]
