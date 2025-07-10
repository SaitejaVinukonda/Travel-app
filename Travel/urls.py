from django.urls import path
from Travel import views
urlpatterns = [
    path('',views.home,name=' '),
    path('home',views.home, name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),
    path('chat/',views.chat,name='chat'),
    path('register/',views.register_view,name='register_view'),
    path('profile/',views.profile_view,name='profile_view'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('tour/',views.tour,name='tour'),
    #path('tour/',views.available_tours,name='available_tours'),
    path('available-tours/', views.available_tours, name='available_tours'),
    path('tour_details/<int:id>/',views.tour_details,name='tour_details'),
    path ('blog-details', views.blogDetails, name = 'blogDetails'),
    path('reset-password/<int:user_id>/',views.reset_password,name='reset_password'),
    path('bus_list/', views.bus_list, name='bus_list'),
    path('seats/<int:bus_id>/', views.view_seats, name='view_seats'),
    path('booking-summary/', views.booking_summary, name='booking_summary'),
    path('payment_form/', views.payment_form, name='payment_form'),
    path('payment/<int:bus_id>/', views.payment, name='payment'),
    path('tours/', views.tour_list, name='tour_list'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    #path('logout/', views.logout_view, name='logout_view'),

    #path('hotels/', views.hotel_list, name='hotel_list'),
    #path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    #path('hotels/book/<int:room_id>/', views.book_room, name='book_room'),   
]

