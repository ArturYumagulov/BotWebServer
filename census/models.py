from django.db import models
from tasks.models import Partner, Result, Task


# Create your models here.

class Department(models.Model):
    is_active = models.BooleanField(verbose_name="Активность", default=False)
    name = models.CharField(verbose_name="Имя", max_length=20)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"


class PointTypes(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Тип торговой точки", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='types')

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class PointVectors(models.Model):
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='vectors')
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Имя направления торговой точки", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    slug = models.SlugField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Направленность/Используемые продукты"
        verbose_name_plural = "Направленность/Используемые продукты"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class PointCategory(models.Model):

    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='category')
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Имя категории", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Категория/Сегмент торговой точки"
        verbose_name_plural = "Категории/Сегмент торговых точек"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class CarsList(models.Model):
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='cars')
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
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='oils')
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Марка масла", max_length=500)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    slug = models.SlugField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Список масел торговой точки"
        verbose_name_plural = "Списки масел торговой точки"
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class ProviderList(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Название", max_length=500)
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='providers')
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
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='filters')
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
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='sto_types')
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
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='accessories_category')
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


class Volume(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Название", max_length=500)
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='volume')
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Объем"
        verbose_name_plural = "Объем"


class VolumeItem(models.Model):
    census = models.ForeignKey("Census", on_delete=models.CASCADE, blank=True, default=None)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
    value = models.CharField(verbose_name="Значение", max_length=500, default=0)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.volume}_{self.value}"


class EquipmentList(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Активность")
    name = models.CharField(verbose_name="Название", max_length=500)
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='equipment_list')
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Парк техники"
        verbose_name_plural = "Парк техники"


class EquipmentItem(models.Model):
    census = models.ForeignKey("Census", on_delete=models.CASCADE, blank=True, default=None)
    equipment = models.ForeignKey(EquipmentList, on_delete=models.CASCADE)
    value = models.CharField(verbose_name="Значение", max_length=500, default=None)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.equipment}_{self.value}"


class PointVectorsSelectItem(models.Model):
    is_active = models.BooleanField(default=False)
    vectors = models.ForeignKey(PointVectors, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=1000)
    department = models.ManyToManyField(Department, verbose_name="Подразделение", related_name='point_vectors')
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.name}"


class PointVectorsItem(models.Model):
    census = models.ForeignKey("Census", on_delete=models.CASCADE, blank=True, default=None)
    vectors = models.ForeignKey(PointVectors, on_delete=models.CASCADE)
    value = models.ManyToManyField(PointVectorsSelectItem, related_name="vector_items", blank=True, default=None)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)

    def __str__(self):
        return f"{self.census} - {self.vectors} - {self.value}"


def get_default_task():
    return Task.objects.get(number="00000000001")


class CensusFiles(models.Model):

    census = models.ForeignKey("Census", on_delete=models.CASCADE, verbose_name='Сенсус', related_name="files")
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    file = models.FileField(upload_to=f"uploads/", blank=True, null=True)
    edited = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Фото Сенсус"
        verbose_name_plural = "Фото Сенсусы"
        ordering = ['-created_date']


class CompanyDatabase(models.Model):
    STATUSES = [
        ('ACTIVE', 'действующая'),
        ('LIQUIDATING', 'ликвидируется'),
        ('LIQUIDATED', 'ликвидирована'),
        ('BANKRUPT', 'банкротство'),
        ('REORGANIZING', 'в процессе присоединения к другому юр.лицу, с последующей ликвидацией'),
    ]

    inn = models.CharField(verbose_name="inn", max_length=12, primary_key=True)
    value = models.CharField(verbose_name="Наименование компании", max_length=2000)
    kpp = models.CharField(verbose_name="КПП", max_length=9, blank=True, null=True, default=None)
    ogrn = models.CharField(verbose_name="ОГРН", max_length=50, blank=True, null=True, default=None)
    ogrn_date = models.DateField(verbose_name="Дата выдачи ОГРН", blank=True, null=True, default=None)
    hid = models.CharField(verbose_name="Внутренний идентификатор в Дадате", max_length=2000)
    type = models.CharField(verbose_name="Тип организации", max_length=10, blank=True, null=True, default=None)
    full_with_opf = models.CharField(verbose_name="Наименование компании", max_length=2000, blank=True, null=True,
                                     default=None)
    short_with_opf = models.CharField(verbose_name="Краткое наименование", max_length=1000, blank=True, null=True,
                                      default=None)
    full = models.CharField(verbose_name="Полное наименование без ОПФ", max_length=1000, blank=True, null=True,
                            default=None)
    short = models.CharField(verbose_name="Краткое наименование без ОПФ", max_length=1000, blank=True, null=True,
                             default=None)
    fio_surname = models.CharField(verbose_name="Фамилия ИП", max_length=1000, blank=True, null=True,
                                   default=None)
    fio_name = models.CharField(verbose_name="Имя ИП", max_length=1000, blank=True, null=True,
                                default=None)
    fio_patronymic = models.CharField(verbose_name="Отчество ИП", max_length=1000, blank=True, null=True,
                                      default=None)
    okato = models.CharField(verbose_name="ОКАТО", max_length=11, blank=True, null=True, default=None)
    oktmo = models.CharField(verbose_name="ОКТМО", max_length=50, blank=True, null=True, default=None)
    okpo = models.CharField(verbose_name="ОКПО", max_length=14, blank=True, null=True, default=None)
    okogu = models.CharField(verbose_name="ОКОГУ", max_length=7, blank=True, null=True, default=None)
    okfs = models.CharField(verbose_name="ОКФС", max_length=61, blank=True, null=True, default=None)
    okved = models.CharField(verbose_name="ОКВЭД", max_length=61, blank=True, null=True, default=None)
    okved_type = models.CharField(verbose_name="Версия справочника ОКВЭД (2001 или 2014)", max_length=4, blank=True,
                                  null=True, default=None)
    opf_code = models.CharField(verbose_name="код ОКОПФ", max_length=100, blank=True, null=True, default=None)
    opf_full = models.CharField(verbose_name="полное название ОПФ", max_length=2000, blank=True, null=True,
                                default=None)
    opf_short = models.CharField(verbose_name="краткое название ОПФ", max_length=2000, blank=True, null=True,
                                 default=None)
    opf_type = models.CharField(verbose_name="краткое название ОПФ", max_length=4, blank=True, null=True,
                                default=None)
    management_name = models.CharField(verbose_name="ФИО руководителя", max_length=1000, blank=True, null=True,
                                       default=None)
    management_post = models.CharField(verbose_name="должность руководителя", max_length=1000, blank=True, null=True,
                                       default=None)
    branch_count = models.CharField(verbose_name="Количество филиалов", max_length=1000, blank=True, null=True,
                                    default=None)
    branch_type = models.CharField(verbose_name="Тип подразделения", max_length=1000, blank=True, null=True,
                                   default=None)
    address_value = models.CharField(verbose_name="Адрес одной строкой", max_length=1000, blank=True, null=True,
                                     default=None)
    address_unrestricted_value = models.CharField(verbose_name="адрес одной строкой (полный, с индексом)",
                                                  max_length=1000, blank=True, null=True, default=None)
    address_data = models.CharField(verbose_name="гранулярный адрес", max_length=1000, blank=True, null=True,
                                    default=None)
    address_data_source = models.CharField(verbose_name="адрес одной строкой как в ЕГРЮЛ", max_length=1000, blank=True,
                                           null=True, default=None)
    address_qc = models.CharField(verbose_name="код проверки адреса", max_length=1, blank=True, null=True,
                                  default=None)
    address_latitude = models.CharField(verbose_name="Широта_DADATA", max_length=50, blank=True, null=True,
                                        default=None)
    address_longitude = models.CharField(verbose_name="Долгота_DADATA", max_length=50, blank=True, null=True,
                                         default=None)
    actuality_date = models.DateField(verbose_name="дата последних изменений", blank=True, null=True, default=None)
    registration_date = \
        models.DateField(verbose_name="дата регистрации", blank=True, null=True, default=None)
    liquidation_date = models.DateField(verbose_name="дата ликвидации", blank=True, null=True, default=None)
    status = models.CharField(verbose_name="статус организации", blank=True, null=True, default=None, choices=STATUSES, max_length=500)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.value} - {self.inn}"

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['-created_date']


class Others(models.Model):
    census = models.ForeignKey("Census", on_delete=models.CASCADE, related_name='census_others')
    equipment_name = models.CharField(max_length=2000, null=True, blank=True, default=None)
    vector = models.CharField(max_length=2000, null=True, blank=True, default=None)
    access_brand = models.CharField(max_length=2000, null=True, blank=True, default=None)
    providers = models.CharField(max_length=2000, null=True, blank=True, default=None)
    volume_name = models.CharField(max_length=2000, null=True, blank=True, default=None)
    volume_value = models.CharField(max_length=2000, null=True, blank=True, default=None)
    products = models.CharField(max_length=2000, null=True, blank=True, default=None)


class Decision(models.Model):
    census = models.ForeignKey('Census', on_delete=models.CASCADE, related_name='census_decisions')
    firstname = models.CharField(max_length=2000, verbose_name="Фамилия", null=True, blank=True)
    lastname = models.CharField(max_length=2000, verbose_name="Имя", null=True, blank=True)
    surname = models.CharField(max_length=2000, verbose_name="Отчество", null=True, blank=True)
    email = models.EmailField(verbose_name="ЛПР_email", null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон", max_length=20, null=True, blank=True)
    function = models.CharField(verbose_name="Должность", max_length=300, null=True, blank=True)


class Census(models.Model):

    address_id = models.PositiveBigIntegerField(verbose_name="ID адреса в 1С")
    department = models.ForeignKey(Department, verbose_name="Подразделение", on_delete=models.PROTECT, default=None)
    address = models.CharField(verbose_name="Адрес", max_length=2000, blank=True, null=True)
    name = models.CharField(verbose_name="Название", max_length=1000, blank=True, null=True)
    point_name = models.CharField(max_length=1000, verbose_name="Вывеска", blank=True, null=True,
                                  default=None)
    point_type = models.ForeignKey(PointTypes, on_delete=models.PROTECT, verbose_name="Тип", blank=True, null=True,
                                   default=None)
    nets = models.BooleanField(verbose_name="Сетевой", default=False)
    sto_type = models.ForeignKey(STOTypeList, on_delete=models.PROTECT, verbose_name="Тип СТО", blank=True, null=True)
    category = models.ForeignKey(PointCategory, on_delete=models.PROTECT, verbose_name="Категория", blank=True, null=True,
                                 default=None)
    cars = models.ManyToManyField(CarsList, verbose_name="Автомобили обслуживают", blank=True, default=None)
    providers = models.ManyToManyField(ProviderList, verbose_name="Основные поставщики", blank=True, default=None)
    elevators_count = models.PositiveIntegerField(verbose_name="Количество подъемников", default=0, null=True,
                                                  blank=True)
    decision = models.ForeignKey(Decision, on_delete=models.SET_NULL, verbose_name="Контактное лицо", null=True,
                                 blank=True, default=None, related_name="decision")
    akb_specify = models.BooleanField(default=False, verbose_name="Специализированная точка по АКБ?")
    working = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name="Контрагент в 1С", blank=True,
                                null=True)
    edit_date = models.DateField(verbose_name="Дата изменения", auto_now=True)
    created_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    edited = models.BooleanField(default=False)
    result = models.ForeignKey(Result, on_delete=models.SET_NULL, verbose_name="Результат встречи", null=True,
                               blank=True, default=None)
    task = models.CharField(verbose_name='Номер задачи', null=True, blank=True, max_length=1000)
    inn = models.CharField(verbose_name="ИНН", max_length=12, blank=True, null=True, default=None)
    volume = models.ManyToManyField(VolumeItem, blank=True, related_name='census_volumes')
    equipment = models.ManyToManyField(EquipmentItem, related_name='census_equipments', blank=True, default=None)
    organizations_name = models.CharField(verbose_name="Название организации", max_length=2000, blank=True, null=True)
    tender = models.BooleanField(verbose_name="Тендер", default=False)
    closing = models.BooleanField(verbose_name="Точка закрыта", default=False)
    not_communicate = models.BooleanField(verbose_name="Нет коммуникации", default=False)
    position = models.CharField(verbose_name="Местоположение", max_length=100, blank=True, null=True)
    dadata = models.ForeignKey('CompanyDatabase', on_delete=models.SET_NULL, blank=True, null=True,
                               default=None)
    vectors = models.ManyToManyField(PointVectorsItem, blank=True, default=None, related_name='census_vectors')
    others = models.ForeignKey("Others", on_delete=models.CASCADE, blank=True, null=True, default=None,
                               related_name='census_others')
    basics = models.CharField(verbose_name='Номер основания', null=True, blank=True, max_length=1000)

    class Meta:
        verbose_name = "Сенсус"
        verbose_name_plural = "Сенсусы"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.address_id}"


