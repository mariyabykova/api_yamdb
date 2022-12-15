from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleListSerializer,
    TitleSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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


class CommentViewSet(viewsets.ModelViewSet):
    """Получение/создание/обновление/удаление
    комментария к отзыву о произведении
    """
    serializer_class = CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Получение списка всех категорий.
    Создание/удаление категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    """Получение списка всех жанров.
    Создание/удаление жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Получение списка всех произведений.
    Получение информации о конкретном произведении.
    Создание/обновление/удаление произведения.
    """
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    # search_fields = ('category__slug',)

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer
