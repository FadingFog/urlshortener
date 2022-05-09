from django.urls import path
from . import views as api


app_name = "api"

urlpatterns = [
    path('links/', api.links),
]
