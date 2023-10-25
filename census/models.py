import django
from django.db import models
from tasks.models import Partner, Result, Task


# Create your models here.


class PointTypes(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Тип торговой точки", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class PointVectors(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Имя направления торговой точки", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Направленность"
        verbose_name_plural = "Направленность"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class PointCategory(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Имя категории", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Категория торговой точки"
        verbose_name_plural = "Категории торговых точек"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class CarsList(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Марка автомобиля", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Список автомобилей торговой точки"
        verbose_name_plural = "Списки автомобилей торговой точки"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class OilList(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Марка масла", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Список масел торговой точки"
        verbose_name_plural = "Списки масел торговой точки"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class ProviderList(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Марка масла", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Список поставщиков торговой точки"
        verbose_name_plural = "Списки поставщиков торговой точки"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class FilterList(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Марка фильтра", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Список фильтров торговой точки"
        verbose_name_plural = "Списки фильтров торговой точки"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class STOTypeList(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Тип СТО", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Список типов СТО торговой точки"
        verbose_name_plural = "Списки типов СТО торговой точки"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class AccessoriesCategory(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Категория аксессуаров", max_length=1000)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Список категорий аксессуаров"
        verbose_name_plural = "Списки категорий аксессуаров"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class AccessoriesCategoryItem(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Марка", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    category = models.ForeignKey(AccessoriesCategory, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = "Список брендов в категории аксессуаров"
        verbose_name_plural = "Списки брендов в категории аксессуаров"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


def get_default_task():
    return Task.objects.get(number="00000000001")


class Census(models.Model):
    address_id = models.PositiveBigIntegerField(verbose_name="ID адреса в 1С")
    address = models.CharField(verbose_name="Адрес", max_length=2000, blank=True, null=True)
    name = models.CharField(verbose_name="Название", max_length=1000, blank=True, null=True)
    point_name = models.CharField(max_length=1000, verbose_name="Вывеска", blank=True, null=True,
                                  default=None)
    point_type = models.ForeignKey(PointTypes, on_delete=models.PROTECT, verbose_name="Тип", blank=True, null=True,
                                   default=None)
    vector = models.ManyToManyField(PointVectors, verbose_name="Направленность", blank=True, default=None)
    other_vector = models.CharField(verbose_name="Другое направление", max_length=1000, blank=True, null=True,
                                    default=None)
    nets = models.BooleanField(verbose_name="Сетевой", default=False)
    sto_type = models.ForeignKey(STOTypeList, on_delete=models.PROTECT, verbose_name="Тип СТО", blank=True, null=True)
    category = models.ForeignKey(PointCategory, on_delete=models.PROTECT, verbose_name="Категория", blank=True, null=True,
                                 default=None)
    cars = models.ManyToManyField(CarsList, verbose_name="Автомобили обслуживают", blank=True, default=None)
    oils = models.ManyToManyField(OilList, verbose_name="Масла используют", blank=True, default=None)
    providers = models.ManyToManyField(ProviderList, verbose_name="Основные поставщики", blank=True, default=None)
    filters = models.ManyToManyField(FilterList, verbose_name="Фильтры используют", blank=True, default=None)
    accessories_category = models.ForeignKey(AccessoriesCategory, verbose_name="Категории аксессуаров",
                                             on_delete=models.PROTECT, blank=True, default=None, null=True)
    accessories_brands = models.ManyToManyField(AccessoriesCategoryItem, verbose_name="Бренды аксессуаров", blank=True,
                                                default=None)
    elevators_count = models.PositiveIntegerField(verbose_name="Количество подъемников", default=0, null=True,
                                                  blank=True)
    oil_debit = models.PositiveIntegerField(default=0, null=True, blank=True)
    lukoil_debit = models.PositiveIntegerField(default=0, null=True, blank=True)
    rowe_debit = models.PositiveIntegerField(default=0, null=True, blank=True)
    motul_debit = models.PositiveIntegerField(default=0, null=True, blank=True)
    decision_fio = models.CharField(max_length=2000, verbose_name="ЛПР_ФИО", null=True, blank=True)
    decision_email = models.EmailField(verbose_name="ЛПР_email", null=True, blank=True)
    decision_phone = models.CharField(verbose_name="Телефон", max_length=20, null=True, blank=True)
    other_brand = models.TextField(verbose_name="Другие бренды аксессуаров", blank=True, null=True)
    akb_specify = models.BooleanField(default=False, verbose_name="Специализированная точка по АКБ?")
    working = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name="Контрагент в 1С", blank=True,
                                null=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edited = models.BooleanField(default=False)
    result = models.ForeignKey(Result, on_delete=models.SET_NULL, verbose_name="Результат встречи", null=True,
                               blank=True, default=None)
    other_providers = models.CharField(max_length=1000, verbose_name="Другие поставщики", blank=True, null=True,
                                       default=None)
    task = models.CharField(verbose_name='Номер задачи', null=True, blank=True, max_length=1000)
    inn = models.CharField(verbose_name="ИНН", max_length=12, blank=True, null=True, default=None)
    organizations_name = models.CharField(verbose_name="Название организации", max_length=2000, blank=True, null=True)
    closing = models.BooleanField(verbose_name="Точка закрыта", default=False)

    class Meta:
        verbose_name = "Сенсус"
        verbose_name_plural = "Сенсусы"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.address_id}"
