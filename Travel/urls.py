from django.urls import path
from Travel import views
urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home, name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register_view,name='register_view'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('tour/',views.tour,name='tour'),

    path('bus_list/', views.bus_list, name='bus_list'),
    path('seats/<int:bus_id>/', views.view_seats, name='view_seats'),
    path('booking-summary/', views.booking_summary, name='booking_summary'),
    path('payment/<int:bus_id>/', views.payment, name='payment'),
]

