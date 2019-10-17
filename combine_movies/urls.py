from django.urls import path
from . import views

urlpatterns = [
	path('', views.home),
    path('<str:movie1>/<str:movie2>', views.combine),
]
