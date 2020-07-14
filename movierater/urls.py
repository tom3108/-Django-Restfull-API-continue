from django.urls import include
from api import urls
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
    path('api-token-auth/', views.obtain_auth_token)
]
