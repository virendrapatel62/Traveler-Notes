from django.forms.forms import Form
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login

# Create your views here.


def home(request):
    return HttpResponse(f"Hello {request.user}")


class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'authforms/signup.html'
    success_url = 'login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'authforms/login.html'
    success_url = '/'

    def form_valid(self, form):
        # form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request=self.request, user=user)
        return super().form_valid(form)
