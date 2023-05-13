from django.db import models


# Create your models here.
class Basics(models.Model):
    name = models.CharField(verbose_name="Название", max_length=1000)
    date = models.DateTimeField(verbose_name="Дата основания")
    number = models.CharField(verbose_name="Номер", max_length=11, primary_key=True)

    def __str__(self):
        return f"{self.name} {self.number} {self.date}"


class Partner(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=1000)
    code = models.CharField(verbose_name="Код 1С", max_length=11, primary_key=True)

    def __str__(self):
        return f"{self.name}"


class Worker(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=1000)
    code = models.CharField(verbose_name="Код 1С", primary_key=True, max_length=11)
    chat_id = models.IntegerField(unique=True, blank=True, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class AuthorComments(models.Model):
    comment = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return f"{self.comment} {self.author}"


class WorkerComments(models.Model):
    comment = models.TextField(verbose_name="Комментарий")
    worker = models.ForeignKey(Worker, verbose_name="Исполнитель", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} {self.worker}"


class Task(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Имя")
    number = models.CharField(max_length=11, verbose_name="Номер", primary_key=True)
    date = models.DateTimeField(verbose_name="Дата")
    status = models.CharField(max_length=100, verbose_name="Статус", default="Новая")
    deadline = models.DateTimeField(verbose_name="Исполнить до")
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name="Исполнитель",
                               related_name="task_worker", default="Удален")
    partner = models.ForeignKey(Partner, verbose_name="Контрагент", max_length=1000, on_delete=models.CASCADE,
                                related_name="partner_tasks")
    author = models.ForeignKey(Worker, verbose_name="Автор", on_delete=models.CASCADE, related_name="task_author")

    author_comment = models.ForeignKey(AuthorComments,
                                       verbose_name="Комментарий автора",
                                       on_delete=models.CASCADE,
                                       related_name='author_comments')
    worker_comment = models.ForeignKey(WorkerComments,
                                       verbose_name="Комментарий исполнителя",
                                       on_delete=models.CASCADE,
                                       related_name='worker_comments')

    base = models.ForeignKey(Basics, verbose_name="Основание", on_delete=models.CASCADE, related_name='base_tasks')
    edited = models.BooleanField(verbose_name="изменен", default=False)

    def __str__(self):
        return f"{self.name} {self.number} {self.deadline}"
