import csv

from django.apps import apps
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from ...models import Comment, Category, Genre, Title, TitleGenre, Review, User


class Command(BaseCommand):
    help = 'Creating model objects according the file path specified'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="file path")
        parser.add_argument('--model_name', type=str, help="model name")
        parser.add_argument(
            '--app_name',
            type=str,
            help="django app name that the model is connected to"
        )

    def handle(self, *args, **options):
        file_path = options['path']
        model = apps.get_model(options['app_name'], options['model_name'])
        with open(file_path, 'rt', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')

            if model in [Category, Genre]:
                for row in reader:
                    model.objects.create(**row)

            elif model == Title:
                for row in reader:
                    Title.objects.create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=get_object_or_404(Category, pk=row['category']),
                    )

            elif model == TitleGenre:
                for row in reader:
                    TitleGenre.objects.create(
                        id=row['id'],
                        title=get_object_or_404(Title, pk=row['title_id']),
                        genre=get_object_or_404(Genre, pk=row['genre_id']),
                    )

            elif model == Comment:
                for row in reader:
                    Comment.objects.create(
                        id=row['id'],
                        review=get_object_or_404(Review, pk=row['review_id']),
                        text=row['text'],
                        author=get_object_or_404(User, pk=row['author']),
                        pub_date=row['pub_date'],
                    )

            elif model == Review:
                for row in reader:
                    Review.objects.create(
                        id=row['id'],
                        title=get_object_or_404(Title, pk=row['title_id']),
                        text=row['text'],
                        author=get_object_or_404(User, pk=row['author']),
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
