import copy

from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from django.core import serializers
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from .forms import CreateUserForm, CreateUrlForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Url


def home(request):
    if request.method == 'POST':
        form = CreateUrlForm(request.POST)

        if form.is_valid():  # AJAX
            url = form.save(commit=False)

            if request.user.is_authenticated:
                url.owner = request.user
                url.save()
            else:  # If link already exists and user not logged in - return the existing
                try:
                    url.hash_url = Url.objects.filter(full_url=form.cleaned_data.get('full_url'),
                                                      owner=None).first().hash_url
                except:
                    url.save()

            message = 'Short link successfully created!'
            form_data = model_to_dict(form.instance)
            html = render_to_string('results.html', {'form_data': form_data, 'request': request})

            data = {'status': 200, 'message': message, 'html': html}
            return JsonResponse(data)
        else:
            data = {'status': 400, 'errors': form.errors}
            return JsonResponse(data)

    else:
        form = CreateUrlForm()

    return render(request, 'index.html', {'form': form})


@login_required
def accountPage(request):
    user_urls = Url.objects.filter(owner=request.user)

    context = {'user_urls': user_urls}
    return render(request, 'dashboard/account.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.info(request, f'Now you can log in as {user}')

            return redirect('login')
    else:
        form = CreateUserForm()

    return render(request, 'register.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('home')

    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, 'Welcome back, ' + username)
                return redirect('home')
            else:
                messages.warning(request, 'Username or password is incorrect')
    else:
        form = LoginUserForm

    return render(request, 'login.html', {'form': form})


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
