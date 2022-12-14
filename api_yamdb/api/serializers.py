from rest_framework import serializers

from reviews.models import Comment, Review, User


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

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
