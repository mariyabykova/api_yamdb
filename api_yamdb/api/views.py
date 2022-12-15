from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .permissions import IsModeratorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer)


class SignUpView(generics.CreateAPIView):
    """Регистрация нового пользователя по username и email.
    На электронную почту пользователю отправляется
    код подтверждения.
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Получение кода подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}.',
            from_email=settings.EMAIL_ADMIN,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение/создание/обновление/удаление
    отзыва к произведению
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Получение/создание/обновление/удаление
    комментария к отзыву о произведении
    """
    serializer_class = CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination
