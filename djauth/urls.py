from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('more/', views.more, name='more'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('search/', include('users.urls')),
]
