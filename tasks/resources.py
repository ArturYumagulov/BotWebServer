from import_export import resources

from .models import Task


class TaskResource(resources.ModelResource):

    class Meta:
        model = Task
        fields = ('name', 'number', 'date', 'status', 'deadline', 'edit_date', 'worker__name', 'partner__name',
                  'author__name', 'author_comment__comment', 'worker_comment__comment', 'base', 'edited',
                  'result__type', 'message_id')
