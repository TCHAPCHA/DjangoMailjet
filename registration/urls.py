from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.register_success, name='register_success'),
]