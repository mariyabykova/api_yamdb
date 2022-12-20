import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from ...models import Comment, Genre, Title, TitleGenre, Review, User


class Command(BaseCommand):
    help = 'Load reviews csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Review.objects.create(
                    id=row[0],
                    title=get_object_or_404(Title, pk=row[1]),
                    text=row[2],
                    author=get_object_or_404(User, pk=row[3]),
                    score=row[4],
                    pub_date=row[5],
                )
