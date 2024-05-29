from django.urls import path, include
from rest_framework.authtoken import views as auth_view
from rest_framework.routers import DefaultRouter

from tasks.models import Task, Worker, PartnerWorker
from api.serializers import tasks
from api.views import task_views, census_views

router = DefaultRouter()
router.get_api_root_view().cls.__name__ = "Tasks & Census_API"
router.get_api_root_view().cls.__doc__ = "API для бота по задачам из 1С"

router.register('base', task_views.BaseViewSet, basename="base")
router.register('tasks', task_views.TaskViewSet, basename='tasks')
router.register('all-tasks', task_views.TaskViewListSet, basename="all_tasks")
router.register('all-tasks-update', task_views.AllTasksUpdateView, basename="all_tasks_update")
router.register('partners', task_views.PartnersViewSet, basename='partners')
router.register('partners-worker', task_views.PartnersWorkerViewSet, basename="partners_worker_list")
router.register('workers', task_views.WorkerViewSet)
router.register('supervisors', task_views.SupervisorViewSet, basename="supervisors_list")
router.register('author_comment', task_views.AuthorCommentsViews, basename="author_comments")
router.register('worker_comment', task_views.WorkerCommentsViews, basename="worker_comment")
router.register('result', task_views.ResultListView, basename='result_list')
router.register('result-group', task_views.ResultGroupListView, basename='result_group_list')
router.register('result-data', task_views.ResultDataListView, basename='result_data_list')
router.register('census', census_views.CensusView, basename='census')
# router.register('census-update', views.CensusUpdate, basename='census_update')
router.register('task-message-update', task_views.TaskMessageUpdateView, basename='task_message_update')


# Фильтры
urlpatterns = [
    path('token-auth/', auth_view.obtain_auth_token, name="api_login"),
    path('', include(router.urls), name="api"),
    path('tasks_f/', task_views.TasksFilterViews.as_view(
        queryset=Task.objects.all(),
        serializer_class=tasks.TaskListSerializer),
        name='tasks_list'),
    path('worker_f/', task_views.WorkerFilterViews.as_view(
        queryset=Worker.objects.all(),
        serializer_class=tasks.WorkerSerializer),
        name='workers_filter'),
    path('partner-worker_f/', task_views.PartnerWorkerFilterViews.as_view(
        queryset=PartnerWorker.objects.all(),
        serializer_class=tasks.PartnerWorkerSerializer),
         name='partner-worker_filter'),
    path('result-data_f/', task_views.ResultDataFilterViews.as_view(), name='result_filter'),
    path('partner_f/', task_views.PartnerFilterViews.as_view(), name='partner_filter'),
    path('census-task/', census_views.CensusFilterViews.as_view(), name='census_filter'),
]
