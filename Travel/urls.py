from django.urls import path
from Travel import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
]