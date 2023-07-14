from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from .swagger import swaggerurlpatterns


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("preventa/", include("apps.preventa.urls")),
    path("payment/", include("apps.payment.urls")),
    re_path(r"^accounts/", include("allauth.urls"), name="socialaccount_signup"),
]

urlpatterns += swaggerurlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
