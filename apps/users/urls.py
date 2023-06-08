from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


application_urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns = application_urlpatterns
