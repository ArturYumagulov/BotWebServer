import logging
from django.utils.timezone import make_aware

from datetime import datetime, timedelta
from celery import shared_task

from tasks.models import Task, WorkerComments, AuthorComments


logger = logging.getLogger(__name__)


@shared_task
def del_task():
    date = datetime.now() - timedelta(days=14)
    del_date = make_aware(date)
    tasks = Task.objects.filter(status="Загружено").filter(deadline__lte=del_date)
    worker_comments = WorkerComments.objects.filter(created_date__lte=del_date)
    worker_comments_length = len(worker_comments)
    if worker_comments_length > 0:
        worker_comments.delete()
        logger.info(f"Celery удалены комментарии исполнителей - {worker_comments_length} шт. - {datetime.now()}")
        print(f"Celery удалены комментарии исполнителей - {worker_comments_length} шт. - {datetime.now()}")

    author_comments = AuthorComments.objects.filter(created_date__lte=del_date)
    author_comments_length = len(author_comments)
    if author_comments_length > 0:
        author_comments.delete()
        logger.info(f"Celery удалены комментарии авторов - {author_comments_length} шт. - {datetime.now()}")
        print(f"Celery удалены комментарии авторов - {author_comments_length} шт. - {datetime.now()}")

    if len(tasks) > 0:
        for task in tasks:
            task_number = task.number
            task.delete()
            logger.info(f"Celery удалена задача номер {task_number} - {datetime.now()}")
            print(f"Celery удалена задача номер {task_number} - {datetime.now()}")
            return True
    else:
        return True
