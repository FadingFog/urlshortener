from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from rest_framework.authtoken.models import Token

from .models import Url
from .forms import CreateUserForm, CreateUrlForm, LoginUserForm, ResetPasswordForm, SetPasswordForm


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

            data = {'message': message, 'html': html}
            return JsonResponse(data, status=200)
        else:
            data = {'errors': form.errors.get_json_data()}
            return JsonResponse(data, status=400)

    else:
        form = CreateUrlForm()

    return render(request, 'index.html', {'form': form})


@login_required(login_url='login')
def accountPage(request):
    user_urls = Url.objects.filter(owner=request.user)

    paginator = Paginator(user_urls, 3)
    page = request.GET.get('page')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context = {'object_list': object_list}
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def integrationsPage(request):
    tokens = Token.objects.filter(user=request.user)

    context = {'tokens': tokens}
    return render(request, 'dashboard/integrations.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('home')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            message = f'Now you can log in as {user}'

            data = {'message': message}
            return JsonResponse(data, status=200)
        else:
            data = {'errors': form.errors.get_json_data()}
            return JsonResponse(data, status=400)
    else:
        form = CreateUserForm()

    return render(request, 'register.html', {'form': form})


def loginPage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('home')

    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            message = f'Welcome back, {user.username}'
            data = {'message': message}
            return JsonResponse(data, status=200)
        else:
            data = {'errors': form.errors.get_json_data()}
            return JsonResponse(data, status=400)

    else:
        form = LoginUserForm

    return render(request, 'login.html', {'form': form})


def logoutPage(request):
    logout(request)
    return redirect('home')


def redirectURL(request, hash_url):
    try:
        url = Url.objects.get(hash_url=hash_url)  # TODO Replace by get_object_or_404()
        url.clicks += 1
        url.save()
        return redirect(url.full_url)
    except:
        raise Http404  # That URL doesn't exist


class ResetPasswordView(PasswordResetView):
    template_name = "password_reset.html"
    form_class = ResetPasswordForm

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return render(self.request, 'password_reset_done.html', status=200)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form), status=404)


class ResetPasswordConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        user = form.save()
        del self.request.session["_password_reset_token"]
        if self.post_reset_login:
            login(self.request, user, self.post_reset_login_backend)
        return render(self.request, 'password_reset_complete.html', status=200)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form), status=404)
