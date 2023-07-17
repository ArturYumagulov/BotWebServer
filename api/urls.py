from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from tasks.models import Task, Worker, PartnerWorker, Result, ResultGroup  # noqa
from .serializers import WorkerSerializer, TaskListSerializer, PartnerWorkerSerializer

from .views import TaskViewSet, BaseViewSet, PartnersViewSet, WorkerViewSet, AuthorCommentsViews, \
    WorkerCommentsViews, TasksFilterViews, WorkerFilterViews, TaskViewListSet, \
    PartnersWorkerViewSet, PartnerWorkerFilterViews, ResultListView, ResultDataFilterViews, ResultGroupListView, \
    ResultDataListView, SupervisorViewSet, AllTasksUpdateView, WorkerDetailView


router = DefaultRouter()
router.get_api_root_view().cls.__name__ = "Tasks_API"
router.get_api_root_view().cls.__doc__ = "API для бота по задачам из 1С"

router.register('base', BaseViewSet, basename="base")
router.register('tasks', TaskViewSet, basename='tasks')
router.register('all-tasks', TaskViewListSet, basename="all_tasks")
router.register('all-tasks-update', AllTasksUpdateView, basename="all_tasks_update")
router.register('partners', PartnersViewSet, basename='partners')
router.register('partners-worker', PartnersWorkerViewSet, basename="partners_worker_list")
router.register('workers', WorkerViewSet)
router.register('supervisors', SupervisorViewSet, basename="supervisors_list")
router.register('author_comment', AuthorCommentsViews, basename="author_comments")
router.register('worker_comment', WorkerCommentsViews, basename="worker_comment")
router.register('result', ResultListView, basename='result_list')
router.register('result-group', ResultGroupListView, basename='result_group_list')
router.register('result-data', ResultDataListView, basename='result_data_list')


# Фильтры
urlpatterns = [
    path('token-auth/', views.obtain_auth_token, name="api_login"),
    path('', include(router.urls), name="api"),
    path('tasks_f/', TasksFilterViews.as_view(queryset=Task.objects.all(), serializer_class=TaskListSerializer),
         name='tasks_list'),
    path('worker_f/', WorkerFilterViews.as_view(queryset=Worker.objects.all(), serializer_class=WorkerSerializer),
         name='workers_filter'),
    path('partner-worker_f/', PartnerWorkerFilterViews.as_view(queryset=PartnerWorker.objects.all(),
                                                               serializer_class=PartnerWorkerSerializer),
         name='partner-worker_filter'),
    path('result-data_f/', ResultDataFilterViews.as_view(), name='result_filter'),
    path('worker_detail/<str:code>/', WorkerDetailView.as_view(), name='worker_detail'),
]


#  TODO добавить авторизацию
