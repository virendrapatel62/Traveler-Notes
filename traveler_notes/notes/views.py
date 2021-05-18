from .models import Note
from django.forms.forms import Form
from django.http import request
from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.


class MyNoteView(ListView):
    template_name = 'notes/my-notes.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


@login_required(login_url='login')
def home(request):
    return render(request=request, template_name='notes/index.html', context={})


@login_required(login_url='login')
def mapView(request):
    return render(request=request, template_name='notes/map_view.html', context={})


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
