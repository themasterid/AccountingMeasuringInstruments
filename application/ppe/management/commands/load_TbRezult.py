import csv

from django.conf import settings
from django.core.management import BaseCommand

from ppe.models import TbRezult


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        data_path = settings.BASE_DIR
        with open(
            f'{data_path}/data/TbRezult.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            TbRezult.objects.bulk_create(
                TbRezult(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS(
            'Все TbRezult загружены!'))
