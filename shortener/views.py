from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *


def index(request):
    urls = Urls.objects.order_by('created_at')
    return render(request, 'index.html', {'urls': urls})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'User {user} successfully created!')

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, username)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def redirectURL(request, hash_url):
    url = Urls.objects.get(hash_url=hash_url)
    url.clicks += 1
    url.save()
    return redirect(url.full_url)
