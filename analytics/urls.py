from django.urls import path

from analytics import views

urlpatterns = [
    path('', views.index, name='analytics'),
    path('report-1/', views.report_1, name="report_1"),
    path('filter-report-1/', views.filter_report_1, name="filter_report_1"),
    path('get-volumes/', views.get_volumes, name="get_volumes"),
    path('save-data/', views.save_on_mongo),
    path('get-lenght/', views.get_length, name="get_len"),
    path('get-volume-sum/', views.get_volumes_sum, name="get_volumes_sum"),
]