from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chat.urls", namespace="chat")),
    path(
        "auth/login/",
        LoginView.as_view(template_name="chat/login.html"),
        name="login",
    ),
    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
