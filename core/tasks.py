import logging
import environ
import requests

from django.utils.timezone import make_aware

from datetime import datetime, timedelta
from celery import shared_task

from analytics import services
from analytics.models import ReportUpdateModel
from analytics.services import create_report_1
from census.services import DataInnOnRedis, unix_to_date
# from parse.services import Parsers
from sales.models import Product
from tasks.models import Task, WorkerComments, AuthorComments, Department, Worker
from census.models import CensusFiles, CompanyDatabase
from send_message.models import SendMessage
from tasks.services import create_worker_secret

logger = logging.getLogger(__name__)

env = environ.Env()
token = env.str("BOT_TOKEN")


@shared_task
def del_task():
    date = datetime.now() - timedelta(days=90)
    del_date = make_aware(date)
    exclude_census = Task.objects.exclude(base__group__name="Сенсус")
    exclude_new = exclude_census.exclude(status="Новая")
    tasks = exclude_new.filter(deadline__lte=del_date)
    worker_comments = WorkerComments.objects.exclude(pk=2).filter(created_date__lte=del_date)
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

    if len(tasks) > 0:
        for task in tasks:
            task_number = task.number
            task.delete()
            logger.info(f"Celery удалена задача номер {task_number} - {datetime.now()}")

    census_files = CensusFiles.objects.filter(created_date__lte=del_date)

    if len(census_files) > 0:
        for file in census_files:
            file_path = file.file
            file.delete()
            logger.info(f"Celery удален файл {file_path} - {datetime.now()}")


@shared_task
def save_organizations(inn):
    data = DataInnOnRedis().get_data(inn)
    if data:
        new_data = CompanyDatabase()
        clean_data = data[0]
        new_data.inn = inn
        new_data.value = clean_data.get('value')
        new_data.kpp = clean_data['data'].get('kpp')
        new_data.ogrn = clean_data['data'].get('ogrn')
        new_data.ogrn_date = unix_to_date(clean_data['data'].get('ogrn_date'))
        new_data.hid = clean_data['data'].get('hid')
        new_data.type = clean_data['data'].get('type')
        new_data.okato = clean_data['data'].get('okato')
        new_data.oktmo = clean_data['data'].get('oktmo')
        new_data.okpo = clean_data['data'].get('okpo')
        new_data.okogu = clean_data['data'].get('okogu')
        new_data.okfs = clean_data['data'].get('okfs')
        new_data.okved = clean_data['data'].get('okved')
        new_data.okved_type = clean_data['data'].get('okved_type')
        new_data.branch_count = clean_data['data'].get('branch_count')
        new_data.branch_type = clean_data['data'].get('branch_type')
        new_data.address_value = clean_data['data'].get('branch_type')

        # name
        if clean_data['data'].get('name'):
            new_data.full_with_opf = clean_data['data']['name'].get('full_with_opf')
            new_data.short_with_opf = clean_data['data']['name'].get('short_with_opf')
            new_data.full = clean_data['data']['name'].get('full')
            new_data.short = clean_data['data']['name'].get('short')

        # FIO
        if clean_data['data'].get('fio') is not None:
            new_data.fio_surname = clean_data['data']['fio'].get('surname')
            new_data.fio_name = clean_data['data']['fio'].get('name')
            new_data.fio_patronymic = clean_data['data']['fio'].get('patronymic')

        # OPF
        if clean_data['data'].get('opf') is not None:
            new_data.opf_code = clean_data['data']['opf'].get('code')
            new_data.opf_full = clean_data['data']['opf'].get('full')
            new_data.opf_short = clean_data['data']['opf'].get('short')
            new_data.opf_type = clean_data['data']['opf'].get('type')
        # Management
        if clean_data['data'].get('management') is not None:
            new_data.management_name = clean_data['data']['management'].get('name')
            new_data.management_post = clean_data['data']['management'].get('post')

        # Address
        if clean_data['data'].get('address') is not None:
            new_data.address_value = clean_data['data']['address'].get('value')
            new_data.address_unrestricted_value = clean_data['data']['address'].get('unrestricted_value')

        # AddressData
        if clean_data['data']['address'].get('data') is not None:
            new_data.address_data = clean_data['data']['address']['data'].get('region_with_type')
            new_data.address_qc = clean_data['data']['address']['data'].get('qc')
            new_data.address_data_source = clean_data['data']['address']['data'].get('source')
            new_data.address_latitude = clean_data['data']['address']['data'].get('geo_lat')
            new_data.address_longitude = clean_data['data']['address']['data'].get('geo_lon')

        # State
        if clean_data['data'].get('state') is not None:
            new_data.actuality_date = unix_to_date(clean_data['data']['state'].get('actuality_date'))
            new_data.registration_date = unix_to_date(clean_data['data']['state'].get('registration_date'))
            new_data.liquidation_date = unix_to_date(clean_data['data']['state'].get('liquidation_date'))
            new_data.status = clean_data['data']['state'].get('status')

        if new_data.save():
            logger.info(f"{inn} - {new_data.value} - сохранено в БД")
            if DataInnOnRedis().remove_data(inn):
                logger.info(f"{inn} - {new_data.value} - удалено из Redis")
            return True
        return True
    return False


@shared_task
def update_reports_data():
    departs = Department.objects.filter(is_active=True).exclude(name='director')
    if len(departs) > 0:
        for depart in departs:
            new_status = ReportUpdateModel()
            data = create_report_1(depart.name)
            if len(data) > 0:
                services.ReportDataOnMongoDB().insert_many_document(data)
                new_status.name = depart.name
                new_status.date = datetime.now()
                new_status.depart = depart
                new_status.save()
        return True
    return False


@shared_task
def send_message_to_telegram(addresses_list, message):
    sending = []
    dont_send = []
    for address in addresses_list:
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={address}&text={message}'
        result = requests.get(url).json()
        if result['ok']:
            sending.append(Worker.objects.get(chat_id=address).name)
        else:
            dont_send.append(Worker.objects.get(chat_id=address).name)
    SendMessage.objects.update_or_create(message=message, send_list=f"{sending}".replace('[', '').replace(']', ''),
                                         dont_send_list=f"{dont_send}".replace('[', '').replace(']', ''))
    return True


@shared_task
def create_secret():
    workers = Worker.objects.all()
    for worker in workers:
        worker.secret = create_worker_secret(token_len=44, algorithm='HS256')
        worker.save()
    return True


# @shared_task
# def update_price():
#     queryset = Product.objects.all()
#     products = queryset.filter(brand__partkom_code__isnull=False)
#     for product in products:
#         partkom_price = Parsers().partkom(article=product.article, maker_id=product.brand.partkom_code)
#         product.partkom_price = partkom_price
#         product.save()
#     return True
