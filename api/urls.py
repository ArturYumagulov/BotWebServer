from django.urls import path, include
from rest_framework.authtoken import views as auth_view
from rest_framework.routers import DefaultRouter
from tasks.models import Task, Worker, PartnerWorker, Result, ResultGroup  # noqa
from .serializers import WorkerSerializer, TaskListSerializer, PartnerWorkerSerializer

from . import views

router = DefaultRouter()
router.get_api_root_view().cls.__name__ = "Tasks & Census_API"
router.get_api_root_view().cls.__doc__ = "API для бота по задачам из 1С"

router.register('base', views.BaseViewSet, basename="base")
router.register('tasks', views.TaskViewSet, basename='tasks')
router.register('all-tasks', views.TaskViewListSet, basename="all_tasks")
router.register('all-tasks-update', views.AllTasksUpdateView, basename="all_tasks_update")
router.register('partners', views.PartnersViewSet, basename='partners')
router.register('partners-worker', views.PartnersWorkerViewSet, basename="partners_worker_list")
router.register('workers', views.WorkerViewSet)
router.register('supervisors', views.SupervisorViewSet, basename="supervisors_list")
router.register('author_comment', views.AuthorCommentsViews, basename="author_comments")
router.register('worker_comment', views.WorkerCommentsViews, basename="worker_comment")
router.register('result', views.ResultListView, basename='result_list')
router.register('result-group', views.ResultGroupListView, basename='result_group_list')
router.register('result-data', views.ResultDataListView, basename='result_data_list')
router.register('census', views.CensusView, basename='census')
router.register('census-update', views.CensusUpdate, basename='census_update')


# Фильтры
urlpatterns = [
    path('token-auth/', auth_view.obtain_auth_token, name="api_login"),
    path('', include(router.urls), name="api"),
    path('tasks_f/', views.TasksFilterViews.as_view(queryset=Task.objects.all(), serializer_class=TaskListSerializer),
         name='tasks_list'),
    path('worker_f/', views.WorkerFilterViews.as_view(queryset=Worker.objects.all(), serializer_class=WorkerSerializer),
         name='workers_filter'),
    path('partner-worker_f/', views.PartnerWorkerFilterViews.as_view(queryset=PartnerWorker.objects.all(),
                                                                     serializer_class=PartnerWorkerSerializer),
         name='partner-worker_filter'),
    path('result-data_f/', views.ResultDataFilterViews.as_view(), name='result_filter'),
    path('census-task/', views.CensusFilterViews.as_view(), name='census_filter'),
]



