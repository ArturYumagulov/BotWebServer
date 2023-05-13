
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from tasks.models import Task, Worker  # noqa
from .serializers import TaskSerializer, WorkerSerializer


from .views import TaskViewSet, BaseViewSet, PartnersViewSet, WorkerViewSet, AuthorCommentsViews, \
    WorkerCommentsViews, TasksFilterViews, WorkerFilterViews


router = DefaultRouter()

router.register('base', BaseViewSet)
router.register('base/(?P<number>[0-9]+)', BaseViewSet)
router.register('tasks', TaskViewSet)
router.register('tasks/(?P<number>[0-9]+)', TaskViewSet)
# router.register('tasks_f/', TasksFilterViews.as_view(queryset=Task.objects.all(), serializer_class=TaskSerializer),
#                 basename='tasks_list')
router.register('partners', PartnersViewSet)
router.register('partners/(?P<code>[0-9]+)', TaskViewSet)
router.register('workers', WorkerViewSet)
router.register('workers/(?P<code>[0-9]+)', TaskViewSet)
router.register('author_comment', AuthorCommentsViews)
router.register('worker_comment', WorkerCommentsViews)


urlpatterns = [
    path('token-auth/', views.obtain_auth_token, name="api_login"),
    path('', include(router.urls), name="api"),
    path('tasks_f/', TasksFilterViews.as_view(queryset=Task.objects.all(), serializer_class=TaskSerializer),
         name='tasks_list'),
    path('worker_f/', WorkerFilterViews.as_view(queryset=Worker.objects.all(), serializer_class=WorkerSerializer),
         name='tasks_list')
]