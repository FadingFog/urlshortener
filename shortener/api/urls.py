from django.urls import path
from . import views as api


app_name = "api"

urlpatterns = [
    path('', api.get_routes),
    path('auth/', api.obtain_auth_token),
    path('auth/<key>/', api.delete_auth_token),
    path('links/', api.links),
    path('links/info/', api.link_info),
]
