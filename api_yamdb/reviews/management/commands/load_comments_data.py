import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from ...models import Comment, Review, User


class Command(BaseCommand):
    help = 'Load comments csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Comment.objects.create(
                    id=row[0],
                    review=get_object_or_404(Review, pk=row[1]),
                    text=row[2],
                    author=get_object_or_404(User, pk=row[3]),
                    pub_date=row[4],
                )
