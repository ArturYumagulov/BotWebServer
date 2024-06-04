import csv
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand

from sales.models import Product


class Command(BaseCommand):
    help = 'Load data from Product file'

    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / 'data' / 'products.csv'

        with open(datafile, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(islice(csvfile, 0, None))
            for row in reader:
                if len(row['code']) <= 50:
                    Product.objects.get_or_create(code=row['code'].strip(), name=row['name'], article=row['article'],
                                                  brand=row['brand'], access_category=row['access_category'])
                else:
                    continue
