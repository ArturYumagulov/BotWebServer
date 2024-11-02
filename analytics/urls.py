from django.urls import path

from analytics import views

urlpatterns = [
    # ---------------REPORT-1------------------------------------------
    # path('save-data/', views.save_on_mongo),
    path("", views.report_1, name="analytics"),
    path("report-1/", views.get_report_1, name="report_1"),
    path("filter-report-1/", views.filter_report_1, name="filter_report_1"),
    path("get-volumes/", views.get_volumes, name="get_volumes"),
    path("get-lenght/", views.get_length, name="get_len"),
    path("get-volume-sum/", views.get_volumes_sum, name="get_volumes_sum"),
    # ---------------Census-detail------------------------------------------
    path("detail/<int:pk>", views.census_detail, name="census_detail"),
    path("get_vectors/", views.census_vector_data, name="get_vectors"),
    # ---------------REPORT-2------------------------------------------
    # path("report-2/", views.report_2, name="report_2"),
    # path("get-report-2/", views.get_report_2, name="get_report_2"),
    # ---------------REPORT-3------------------------------------------
    path("get-report-3/", views.get_report_3, name="get_report_3"),
    path("report-3/", views.report_3, name="report_3"),

    path("tasks/", views.tasks, name="tasks"),

]
