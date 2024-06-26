from django.db import models

# Create your models here.


class SendMessage(models.Model):
    message = models.TextField(verbose_name='Сообщение')
    send_list = models.TextField(verbose_name="Список получивших")
    dont_send_list = models.TextField(verbose_name="Список не получивших")
    created_date = models.DateField(verbose_name="Дата отправки", auto_now_add=True)

    def __str__(self):
        return f'{self.message} - {self.created_date}'

