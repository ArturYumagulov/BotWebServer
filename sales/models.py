from django.utils import timezone
from django.db import models

from tasks.models import Partner

# Create your models here.


class AccessCategory(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=2000, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'


class Brand(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=2000, unique=True, verbose_name='Название')
    partkom_code = models.CharField(max_length=50, unique=True, verbose_name='Партком', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренды'
        verbose_name_plural = 'Бренд'


class Product(models.Model):
    """
    Хранит информацию о товаре. В этой модели укажите поля:
    id (автоматическое поле, первичный ключ);
    name (название товара);
    price (цена товара);
    description (описание товара).
    """

    code = models.CharField(max_length=50, primary_key=True, verbose_name="Код")
    name = models.CharField(max_length=2000, verbose_name="Наименование")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name="Бренд", blank=True, null=True)
    article = models.CharField(max_length=100, verbose_name="Артикул", blank=True, null=True)
    access_category = models.ForeignKey(AccessCategory, verbose_name="Категория товара", max_length=1000, blank=True,
                                        null=True, on_delete=models.PROTECT)
    edit_date = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Активность', default=False)
    tranzit_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    partkom_price = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_date']
        verbose_name = 'Номенклатуры'
        verbose_name_plural = "Номенклатура"


class RetailUnit(models.Model):
    """Торговая точка"""

    code = models.CharField(max_length=11, primary_key=True, verbose_name="Код")
    partner_name = models.ForeignKey(Partner, on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, blank=True, null=True)
    category = models.CharField(max_length=2000, blank=True, null=True)
    type = models.CharField(max_length=2000, blank=True, null=True)
    address = models.CharField(max_length=2000, verbose_name="Адрес", blank=True, null=True)
    vector = models.CharField(max_length=2000, verbose_name="Направление", blank=True, null=True)
    latitude = models.FloatField(verbose_name="Широта", blank=True, null=True)
    longitude = models.FloatField(verbose_name="Широта", blank=True, null=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    contract = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.partner_name.name} - {self.address}"

    class Meta:
        ordering = ['created_date']
        verbose_name = 'Торговая точка'
        verbose_name_plural = "Торговые точки"


class Order(models.Model):
    """Хранит информацию о заказе"""

    number = models.CharField(max_length=100, verbose_name="Номер", primary_key=True)
    retail_unit = models.ForeignKey(RetailUnit, on_delete=models.CASCADE, verbose_name="Торговая точка")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="Контрагент")
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    sales_date = models.DateField(verbose_name="Дата реализации", default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['created_date']
        verbose_name = 'Реализация'
        verbose_name_plural = "Реализации"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_code = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    price = models.DecimalField(verbose_name="Цена", decimal_places=2, default=0, max_length=100, max_digits=10)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Позиция в реализации'
        verbose_name_plural = 'Позиции в реализации'

    def __str__(self):
        return f"{self.order.number} - {self.item_code.name}"

    def get_cost(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        self.total = self.get_cost()
        super(OrderItem, self).save(*args, **kwargs)
