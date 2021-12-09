from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    re_path(r'^(?P<hash_url>\w{10})/$', redirectURL),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('profile/', accountPage, name='account'),
]
