from django.db import models

from tasks.services import create_worker_secret


class Department(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=False)
    name = models.CharField(verbose_name="Имя", max_length=20)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "12. Подразделение"
        verbose_name_plural = "12. Подразделения"


class ResultGroup(models.Model):
    code = models.CharField(verbose_name="Код 1С", max_length=11, primary_key=True)
    name = models.CharField(verbose_name="Имя группы", max_length=1000)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "07. Группа"
        verbose_name_plural = "07. Группы"


class ResultData(models.Model):
    group = models.ForeignKey(ResultGroup, on_delete=models.CASCADE, related_name="result_dates")
    name = models.CharField(max_length=1000)
    control_data = models.BooleanField(default=False)
    code = models.CharField(verbose_name="Код 1С", max_length=11, primary_key=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "09. Результаты-данные групп"
        verbose_name_plural = "09. Результат-данные группы"


class Result(models.Model):

    TYPES = [
        ('email', "Электронное письмо"),
        ('phone', "Телефонный звонок"),
        ('meet', "Личная встреча"),
        ('e-market', "Электронная торговая площадка"),
        ('postmail', "Почтовое письмо"),
        ('other', "Прочее")]

    base = models.ForeignKey('Basics', verbose_name="Основание", on_delete=models.CASCADE,
                             related_name='result_bases',
                             blank=True,
                             null=True,
                             default=None)
    type = models.CharField(choices=TYPES, max_length=1000, default='other')
    result = models.CharField(max_length=1000)
    task_number = models.ForeignKey('Task', on_delete=models.CASCADE,
                                    related_name='result_task',
                                    blank=True,
                                    null=True,
                                    default=None)
    contact_person = models.CharField(max_length=500)
    control_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Результат {self.base}"

    class Meta:
        verbose_name = "08. Результат задач"
        verbose_name_plural = "08. Результаты задач"
        ordering = ['base__date']


class Basics(models.Model):
    name = models.CharField(verbose_name="Название", max_length=1000)
    date = models.DateTimeField(verbose_name="Дата основания")
    number = models.CharField(verbose_name="Номер", max_length=11, primary_key=True)
    group = models.ForeignKey('ResultGroup', on_delete=models.CASCADE, related_name="basics_groups")

    def __str__(self):
        return f"{self.name} {self.number} {self.date}"

    class Meta:
        verbose_name = "02. Основание"
        verbose_name_plural = "02. Основания"
        ordering = ['-date']


class Partner(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=1000)
    code = models.CharField(verbose_name="Код 1С", max_length=11, primary_key=True)
    inn = models.CharField(max_length=12, verbose_name="ИНН", blank=True, null=True, default=None)
    contract = models.BooleanField(default=False, verbose_name="Договор")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "03. Контрагент"
        verbose_name_plural = "03. Контрагенты"
        ordering = ['name']

    #  TODO добавить наличие договора, и сумму отгрузки, статус обмена


class PartnerWorker(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="workers")
    name = models.CharField(max_length=1000)
    positions = models.CharField(max_length=1000)
    code = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return f"{self.code}: {self.name}"

    class Meta:
        verbose_name = "04. Сотрудники контрагента"
        verbose_name_plural = "04. Сотрудники контрагентов"
        ordering = ['name']


class Worker(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=1000)
    code = models.CharField(verbose_name="Код 1С", primary_key=True, max_length=11)
    chat_id = models.PositiveBigIntegerField(unique=True, blank=True, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=15, null=True, blank=True)
    supervisor = models.ForeignKey('Supervisor', on_delete=models.PROTECT, null=True, blank=True)
    controller = models.BooleanField(default=False)
    partner = models.CharField(max_length=11, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.PROTECT)
    secret = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.secret:  # Генерируем секрет только если его еще нет
            self.secret = create_worker_secret(25, "HS256")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "05. Агент"
        verbose_name_plural = "05. Агенты"
        ordering = ['name']


class Head(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=1000)
    code = models.CharField(verbose_name="Код 1С", primary_key=True, max_length=11)
    chat_id = models.IntegerField(unique=True, blank=True, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=15, null=True, blank=True)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "06. Руководитель"
        verbose_name_plural = "06. Руководители"
        ordering = ['name']


class Supervisor(models.Model):
    head = models.ForeignKey(Head, related_name='supervisors', on_delete=models.PROTECT, verbose_name="РОП",
                             blank=True, null=True, default=None)
    name = models.CharField(verbose_name="Имя", max_length=1000)
    code = models.CharField(verbose_name="Код 1С", primary_key=True, max_length=11)
    chat_id = models.IntegerField(unique=True, blank=True, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=15, null=True, blank=True)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "06. Супервайзер"
        verbose_name_plural = "06. Супервайзеры"
        ordering = ['name']


class AuthorComments(models.Model):
    comment = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name="Автор")
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.comment} {self.author}"

    class Meta:
        verbose_name = "10. Комментарий автора"
        verbose_name_plural = "10. Комментарии автора"


class WorkerComments(models.Model):
    comment = models.TextField(verbose_name="Комментарий")
    worker = models.ForeignKey(Worker, verbose_name="Исполнитель", on_delete=models.CASCADE)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.comment} {self.worker}"

    class Meta:
        verbose_name = "11. Комментарий исполнителя"
        verbose_name_plural = "11. Комментарии исполнителя"


class Task(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Имя")
    number = models.CharField(max_length=36, verbose_name="Номер", primary_key=True)
    date = models.DateTimeField(verbose_name="Дата")
    status = models.CharField(max_length=100, verbose_name="Статус", default="Новая")
    deadline = models.DateTimeField(verbose_name="Исполнить до")
    edit_date = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
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
    edited = models.BooleanField(verbose_name="Изменено", default=False)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="task_results", blank=True, null=True,
                               default=None)
    message_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.number} {self.deadline}"

    class Meta:
        verbose_name = "01. Задача"
        verbose_name_plural = "01. Задачи"
        ordering = ['-date']
