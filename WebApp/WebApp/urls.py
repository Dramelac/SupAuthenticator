from django.contrib import admin
from django.urls import path, include
from SupAuthenticator import urls as app_urls

urlpatterns = [
    path('', include(app_urls)),
    path('admin/', admin.site.urls),
]
