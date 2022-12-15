from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import Comment, Review, Title
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
        if User.objects.filter(username=data['username'], email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError('Пользователь с такими данными уже существует!')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author):
                raise ValidationError('Вы уже оставили отзыв '
                                      'на данное произведение')
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
