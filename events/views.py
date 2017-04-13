from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

from django.forms import ValidationError
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import forms

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('events:login'))

@login_required
def landing(request):
    return render(request, 'events/landing.html')


def register(request):
    if request.POST:
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']

            try:
                user = get_user_model().objects.get(username=username)
                if user:
                    form.add_error(None, ValidationError('This user already exists.'))
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(username=username)
                user.set_password(password)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect(reverse('tracker:login'))

    else:
        form = forms.RegisterForm()
    return render(request, 'events/signup.html', {'form': form})


def login_(request):
    if request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('tracker:home'))
                else:
                    form.add_error(None, ValidationError(
                        "Your account is not active."
                    ))
            else:
                form.add_error(None, ValidationError(
                    "Incorrect email or password"
                ))
    else:
        form = forms.LoginForm()
    return render(request, 'events/login.html', {'form': form})


def home(request):
    return render(request, 'events/landing.html')