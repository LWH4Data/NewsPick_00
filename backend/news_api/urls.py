from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('protected/', views.protected_view, name='protected_view'),
]