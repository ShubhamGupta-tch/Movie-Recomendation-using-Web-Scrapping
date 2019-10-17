from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<str:query>', views.search),
    path('<str:query>/trailer', views.trailer),
]
