from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import CreateUserForm, CreateUrlForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Url


def home(request):
    if request.method == 'POST':
        form = CreateUrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            if request.user.is_authenticated:
                url.owner = request.user
            url.save()
            # full_url = form.cleaned_data.get('full_url')  # Don't remember why it's here
            messages.success(request, f'Short link successfully created!')
            return render(request, 'home.html', {'form': form, 'form_data': form.instance})
        else:
            form.fields['full_url'].widget.attrs['class'] = 'form-control is-invalid'
    else:
        form = CreateUrlForm()

    return render(request, 'home.html', {'form': form})


@login_required
def accountPage(request):
    user_urls = Url.objects.filter(owner=request.user)

    context = {'user_urls': user_urls}
    return render(request, 'account.html', context)


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
