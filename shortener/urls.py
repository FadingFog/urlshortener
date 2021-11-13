from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
]
