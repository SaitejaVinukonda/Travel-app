from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from .models import Bus, Seat,Booking,TravelPackage
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
    packages = TravelPackage.objects.all()
    return render(request, 'TourPackages.html',{'packages': packages})

def bus_list(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')

    if source and destination:
        buses = Bus.objects.filter(source__icontains=source, destination__icontains=destination)
    else:
        buses = Bus.objects.all()
        
    return render(request, 'bus_list.html', {'buses': buses})


def view_seats(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    seats = Seat.objects.filter(bus=bus).order_by('seat_number')

    # Arrange seats in a 4-column grid with aisle
    seat_map = []
    row = []
    for i, seat in enumerate(seats):
        row.append(seat)
        if (i + 1) % 4 == 0:
            seat_map.append(row[:2] + ['aisle'] + row[2:])
            row = []

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')
        selected_seats = Seat.objects.filter(id__in=selected_seat_ids, is_booked=False)
        seat_numbers = [seat.seat_number for seat in selected_seats]
        total_price = bus.price * selected_seats.count()

        # Save selected seat ids in session
        request.session['selected_seat_ids'] = selected_seat_ids
        request.session['selected_seat_numbers'] = seat_numbers
        request.session['bus_id'] = bus.id
        request.session['total_price'] = float(total_price)

        return redirect('booking_summary')

    return render(request, 'view_seat.html', {'bus': bus, 'seat_rows': seat_map})


def booking_summary(request):
    seat_ids = request.session.get('selected_seat_ids', [])
    seat_numbers = request.session.get('selected_seat_numbers', [])
    bus_id = request.session.get('bus_id')
    total_price = request.session.get('total_price', 0)

    bus = get_object_or_404(Bus, id=bus_id)

    return render(request, 'booking_summary.html', {
        'bus': bus,
        'selected_seats': ', '.join(seat_numbers),
        'total_price': total_price
    })

def payment(request, bus_id):
    seat_ids = request.session.get('selected_seat_ids', [])
    seats_to_book = Seat.objects.filter(id__in=seat_ids, is_booked=False)

    # Mark seats as booked
    for seat in seats_to_book:
        seat.is_booked = True
        seat.save()

    # Save booking in DB
    bus = get_object_or_404(Bus, id=bus_id)
    booking = Booking.objects.create(bus=bus)
    booking.seats.set(seats_to_book)

    return render(request, 'payment.html', {
        'message': "Booking Successful!",
        'booked_seats': [seat.seat_number for seat in seats_to_book],
    })