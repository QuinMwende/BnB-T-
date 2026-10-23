from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/rooms/', views.get_rooms, name='get_rooms'),
    path('api/book/', views.book_room, name='book_room'),
]