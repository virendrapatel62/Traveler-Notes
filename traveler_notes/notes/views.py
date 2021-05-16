from django.forms.forms import Form
from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Note , NoteSerializer
from django.core import serializers
# Create your views here.


def home(request):
    return render(request=request, template_name='notes/index.html', context={})


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


@csrf_exempt
def createNote(request):
    print(request.POST)
    title = request.POST.get('title')
    comment = request.POST.get('comment')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    user = request.user
    note = Note(title=title, comment=comment, lat=lat, lng=lng, user=user)
    # save this note object here
    note.save()
    serializer = NoteSerializer(note)
    
    return JsonResponse( serializer.data , safe=False)
