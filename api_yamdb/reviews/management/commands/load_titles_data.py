import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from ...models import Category, Title


class Command(BaseCommand):
    help = 'Load titles csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=get_object_or_404(Category, pk=row[3]),
                )
