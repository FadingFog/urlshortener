from django.http import Http404
from django.shortcuts import render, redirect

from .forms import CreateUserForm, CreateUrlForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Url


def home(request):
    if request.method == 'POST':
        form = CreateUrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.owner = request.user
            url.save()
            full_url = form.cleaned_data.get('full_url')
            messages.success(request, f'Short link successfully created!')
            return render(request, 'home.html', {'form': form, 'f_inst': form.instance.__dict__, 'form_data': form.instance})
    else:
        form = CreateUrlForm()

    return render(request, 'home.html', {'form': form})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
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
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def redirectURL(request, hash_url):
    try:
        url = Url.objects.get(hash_url=hash_url)  # TODO Replace by get_object_or_404()
        url.clicks += 1
        url.save()
        return redirect(url.full_url)
    except:
        raise Http404  # That URL doesn't exists
