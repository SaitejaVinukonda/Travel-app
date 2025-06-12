from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'Contacts.html')
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # or any success page
        else:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})

def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            error = "Passwords do not match"
        elif User.objects.filter(username=username).exists():
            error = "Username already exists"
        elif User.objects.filter(email=email).exists():
            error = "Email already in use"
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            return redirect('login')

    return render(request, 'register.html', {'error': error})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if email exists, then send reset link
        # For now, just show a dummy message
        if email:
            return render(request, 'forgot_password.html', {'message': 'Password reset link sent to your email.'})
        else:
            return render(request, 'forgot_password.html', {'error': 'Email not found.'})
    return render(request, 'forgot_password.html')
def tour(request):
    return render(request, 'TourPackages.html')