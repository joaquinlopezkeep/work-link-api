from django.urls import path
from .views import token
urlpatterns = [
    path('token/', token),
]
