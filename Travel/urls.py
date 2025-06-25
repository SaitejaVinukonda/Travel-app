from django.urls import path
from Travel import views
urlpatterns = [
    path('',views.home,name=' '),
    path('home/',views.home, name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register_view,name='register_view'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
<<<<<<< HEAD
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('tour/',views.tour,name='tour'),
=======
    path('tour/',views.available_tours,name='available_tours'),
>>>>>>> 5cd93d92f968b22e99a670e521350bd803ac11d7
    path('available-tours/', views.available_tours, name='available_tours'),
    path('reset-password/<int:user_id>/',views.reset_password,name='reset_password'),
    path('bus_list/', views.bus_list, name='bus_list'),
    path('seats/<int:bus_id>/', views.view_seats, name='view_seats'),
    path('booking-summary/', views.booking_summary, name='booking_summary'),
    path('payment_form/', views.payment_form, name='payment_form'),
    path('payment/<int:bus_id>/', views.payment, name='payment'),
    path('tours/', views.tour_list, name='tour_list'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback')
    
]

