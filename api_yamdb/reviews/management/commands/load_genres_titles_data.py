import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from ...models import Genre, Title, TitleGenre


class Command(BaseCommand):
    help = 'Load titles_genres csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                TitleGenre.objects.create(
                    id=row[0],
                    title=get_object_or_404(Title, pk=row[1]),
                    genre=get_object_or_404(Genre, pk=row[2]),
                )
