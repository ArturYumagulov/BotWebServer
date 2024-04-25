from django.urls import path

from analytics import views

urlpatterns = [
    path('', views.index, name='analytics'),
    path('report-1/', views.report_1, name="report_1")
]