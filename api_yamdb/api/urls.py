from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpView, TitleViewSet)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("genres", GenreViewSet, basename="genre")
router.register("titles", TitleViewSet, basename="title")
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews'
                r'/(?P<review_id>\d+/coments)',
                CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path("v1/", include(router.urls)),
]
