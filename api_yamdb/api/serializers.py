from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+$',
        max_length=150
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя!'
            )
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'Пользователь с такими данными уже существует!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+$',
        max_length=150
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+$',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+$',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author',
            'score', 'pub_date',
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author',
            'pub_date',
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = ('id', 'rating')
