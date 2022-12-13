from django.urls import include, path

from api.views import SignUpView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
]
