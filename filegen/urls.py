from django.urls import path

from filegen.views import gen_excel_report_1

urlpatterns = [
    path('report-1/', gen_excel_report_1, name='load_to_excel_report_1')
]