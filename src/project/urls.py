from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .custom_token_view import CustomTokenObtainView, CustomTokenRefreshView

urlpatterns = [
    path(
        "api/token/", CustomTokenObtainView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("admin/", admin.site.urls),
    
    # account app
    path("api/account/", include("apps.account.urls")),
    
    # def spectacular api
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/doc/", SpectacularSwaggerView.as_view(url_name="schema"), name="doc"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)