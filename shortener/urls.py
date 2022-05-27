from django.urls import path, re_path, include

from .views import *

urlpatterns = [
    path('', home, name='home'),
    re_path(r'^(?P<hash_url>\w{10})/$', redirectURL),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('reset_password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', accountPage, name='account'),

    path('api/', include("shortener.api.urls", namespace="api")),
]
