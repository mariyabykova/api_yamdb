from rest_framework import serializers

from reviews.models import Comment, Review


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+$',
        max_length=150
    )
    email = serializers.EmailField(required=True, max_length=254)


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
