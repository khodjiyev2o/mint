from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api_endpoints import Login


urlpatterns = [
    path("login/email/send/", Login.SendAuthVerificationCodeView.as_view(), name="send-email"),
    path("login/email/", Login.LoginView.as_view(), name="email-login"),
    path("login/google/", Login.GoogleAuth.as_view(), name="google-login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
