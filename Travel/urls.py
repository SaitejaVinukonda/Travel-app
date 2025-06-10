from django.urls import path
from Travel import views
urlpatterns = [
 
    path('home',views.home, name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register_view,name='register_view'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
]
