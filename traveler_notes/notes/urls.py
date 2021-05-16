
from django.contrib import admin
from django.urls import path
from .views import home, SignupView, LoginView, createNote


urlpatterns = [
    path('', home, name='hompage'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('notes/create', createNote, name='create-note'),
]
