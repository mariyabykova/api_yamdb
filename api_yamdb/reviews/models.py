from django.db import models


class Category(models.Model):
    name = models.CharField(
        blank=False,
        max_length=256,
        verbose_name="Название категории",
        unique=True,
    )
    slug = models.SlugField(
        blank=False,
        max_length=50,
        verbose_name="Slug категории",
        unique=True,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        blank=False,
        max_length=256,
        verbose_name="Название жанра",
        unique=True,
    )
    slug = models.SlugField(
        blank=False,
        max_length=50,
        verbose_name="Slug жанра",
        unique=True,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        blank=False,
        on_delete=models.PROTECT,
        related_name="titles",
        verbose_name="Slug категории",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=False,
        through="TitleGenre",
        verbose_name="Slug жанра",
    )
    name = models.CharField(
        blank=False,
        max_length=200,
        verbose_name="Название",
    )
    year = models.IntegerField(
        blank=False,
        max_length=4,
        verbose_name="Год выпуска",
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title} {self.genre}'
