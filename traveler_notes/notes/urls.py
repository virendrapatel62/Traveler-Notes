
from django.contrib import admin
from django.urls import path
from .views import home, SignupView, LoginView, mapView, MyNoteView
from .api_views import NoteDetailView, NoteListView, PlaceSearchApiView, ElocApiView


urlpatterns = [
    path('', home, name='hompage'),
    path('my-notes', MyNoteView.as_view(), name='mynotes'),
    path('notes/map', mapView, name='mapview'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),

    path('api/notes', NoteListView.as_view(), name='note-list'),
    path('api/notes/<int:pk>', NoteDetailView.as_view(), name='note-detail'),
    path('api/map/search/places', PlaceSearchApiView.as_view(), name='search-view'),
    path('api/map/eloc/<str:placeid>', ElocApiView.as_view(), name='eloc-view'),
]
