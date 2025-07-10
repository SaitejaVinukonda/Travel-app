from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour,Bus, Seat,Booking,TravelPackage
from Tourism import settings
from django.core.mail import send_mail
from .models import CustomUser
from django.contrib import messages
import random
from .utils import sendOTPtOEmail
from django.db import transaction
from django.db.models import Q
from .models import Hotel, HotelRoom, HotelBooking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
# from django.contrib.auth import logout

#from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#from google.cloud import dialogflow_v2 as dialogflow
#import uuid
#import json

# Load environment variables from .env
#load_dotenv()
#
## Set the path to the service account key
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
#
## Replace with your Dialogflow project ID
#PROJECT_ID = 'travelassistant-9epl'  


#rf_exempt
#def chat_with_bot(request):
#    if request.method == 'POST':
#        try:
#            data = json.loads(request.body)
#            user_message = data.get('message', '')
#
#            if not user_message:
#                return JsonResponse({'error': 'No message provided'}, status=400)
#
#            # Generate a unique session ID per user (or use Django session ID)
#            SESSION_ID = str(uuid.uuid4())
#
#            session_client = dialogflow.SessionsClient()
#            session = session_client.session_path(PROJECT_ID, SESSION_ID)
#
#            text_input = dialogflow.TextInput(text=user_message, language_code="en")
#            query_input = dialogflow.QueryInput(text=text_input)
#
#            response = session_client.detect_intent(
#                request={"session": session, "query_input": query_input}
#            )
#
#            bot_reply = response.query_result.fulfillment_text
#
#            return JsonResponse({"reply": bot_reply})
#        
#        except Exception as e:
#            return JsonResponse({'error': str(e)}, status=500)
#    else:
#        return JsonResponse({'error': 'Invalid request method'}, status=405) 
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'Contacts.html')
from django.shortcuts import render, redirect
from .models import CustomUser, PasswordResetRequest
from django.contrib.auth.hashers import make_password, check_password

def login_view(request):
    # ✅ If already logged in, redirect to profile
    if request.session.get('user_id'):
        return redirect('profile_view')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('profile_view')
            else:
                error = "Invalid username or password"
        except CustomUser.DoesNotExist:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})
def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_view')

    try:
        user = CustomUser.objects.get(id=user_id)
        bookings = Booking.objects.filter(user=user).select_related('bus')
    except CustomUser.DoesNotExist:
        return redirect('login_view')

    return render(request, 'profile.html', {'user': user, 'bookings': bookings})


def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            error = "Passwords do not match"
        elif CustomUser.objects.filter(username=username).exists():
            error = "Username already exists"
        elif CustomUser.objects.filter(email=email).exists():
            error = "Email already in use"
        else:
            hashed_password = make_password(password1)
            CustomUser.objects.create(username=username, email=email, password=hashed_password)
            return redirect('login_view')

    return render(request, 'register.html', {'error': error})

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, "Email is required.")
            return redirect('login_view')

        custom_user = CustomUser.objects.filter(email=email)
        if not custom_user.exists():
            messages.warning(request, "No account found with this email.")
            return redirect('login_view')

        otp = random.randint(1000, 9999)
        custom_user.update(otp=otp)

        try:
            sendOTPtOEmail(email, otp)
            messages.success(request, f"OTP sent to {email}")
        except Exception as e:
            messages.error(request, f"Failed to send OTP: {str(e)}")
            return redirect('login_view')

        return render(request, 'otp.html', {'email': email})

    # ✅ Render blank OTP form when user clicks "Login with OTP"
    return render(request, 'otp.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_input = request.POST.get('otp')

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No account found.")
            return redirect('login_view')

        if str(user.otp) == str(otp_input):
            messages.success(request, "OTP verified successfully!")
            request.session['user_id'] = user.id  # or login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP.")
            return render(request, 'otp.html', {'email': email})
   
#def enter_otp(request, email):
#    return render(request, 'otp.html', {'email': email})
def reset_password(request, user_id):
    error = success = ''
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error = 'Passwords do not match.'
        else:
            try:
                user = CustomUser.objects.get(id=user_id)
                user.password = password1  
                user.save()
                success = 'Password reset successful.'
                return redirect('login_view')
            except CustomUser.DoesNotExist:
                error = 'Invalid link.'
    return render(request, 'reset_password.html', {'error': error, 'success': success})
def tour(request):
    packages = TravelPackage.objects.all()
    return render(request, 'TourPackages.html',{'packages': packages})

#@login_required
def tour(request):
    packages = TravelPackage.objects.all()
    return render(request, 'TourPackages.html',{'packages': packages})
#@login_required

def bus_list(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')

    if source and destination:
        buses = Bus.objects.filter(source__icontains=source, destination__icontains=destination)
    else:
        buses = Bus.objects.all()
        
    return render(request, 'bus_list.html', {'buses': buses})
#@login_required
#@login_required
def view_seats(request, bus_id):

    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please log in to book a seat.")
        return redirect('login_view')

    bus = get_object_or_404(Bus, id=bus_id)
    seats = Seat.objects.filter(bus=bus).order_by('seat_number')
    seat_map = []
    row = []
    for i, seat in enumerate(seats):
        row.append(seat)
        if (i + 1) % 4 == 0:
            seat_map.append(row[:2] + ['aisle'] + row[2:])
            row = []
    if row:
        seat_map.append(row)
    all_seats_booked = all(seat.is_booked for seat in seats)
    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')
        selected_seats = Seat.objects.filter(id__in=selected_seat_ids, is_booked=False)
        if not selected_seats:
            return render(request, 'view_seat.html', {
                'bus': bus,
                'seat_rows': seat_map,
                'error': "No valid seats selected.",
                'all_seats_booked': all_seats_booked
            })

        seat_numbers = [seat.seat_number for seat in selected_seats]
        total_price = bus.price * selected_seats.count()

        request.session['selected_seat_ids'] = selected_seat_ids
        request.session['selected_seat_numbers'] = seat_numbers
        request.session['bus_id'] = bus.id
        request.session['total_price'] = float(total_price)

        return redirect('booking_summary')

    return render(request, 'view_seat.html', {
        'bus': bus,
        'seat_rows': seat_map,
        'all_seats_booked': all_seats_booked
    })
#@login_required
def booking_summary(request):
    seat_ids = request.session.get('selected_seat_ids', [])
    seat_numbers = request.session.get('selected_seat_numbers', [])
    bus_id = request.session.get('bus_id')
    tour_id = request.session.get('tour_id')

    # Convert float from session to Decimal
    total_price = Decimal(str(request.session.get('total_price', 0)))

    bus = get_object_or_404(Bus, id=bus_id)
    tour = get_object_or_404(Tour, id=tour_id)
    tour_price = tour.price  # Already a Decimal

    # Add both Decimals safely
    grand_total = total_price + tour_price

    return render(request, 'booking_summary.html', {
        'bus': bus,
        'selected_seats': ', '.join(seat_numbers),
        'total_price': total_price,
        'tour': tour,
        'tour_price': tour_price,
        'grand_total': grand_total
    })

#@login_required
#@login_required
def payment_form(request):
    bus_id = request.session.get('bus_id')
    seat_ids = request.session.get('selected_seat_ids', [])
    tour_id = request.session.get('tour_id')  # Get tour ID

    if not bus_id or not seat_ids or not tour_id:
        return HttpResponseBadRequest("Missing booking info.")

    bus = get_object_or_404(Bus, id=bus_id)
    tour = get_object_or_404(Tour, id=tour_id)
    seats = Seat.objects.filter(id__in=seat_ids)

    # Compute prices
    bus_total = float(bus.price) * len(seats)
    tour_price = float(tour.price)  # Convert Decimal to float safely
    total_price = bus_total + tour_price

    return render(request, 'payment_form.html', {
        'bus_id': bus_id,
        'total_price': total_price
    })


@transaction.atomic
def payment(request, bus_id):
    
    seat_ids = request.session.get('selected_seat_ids', [])
    if not seat_ids:
        return HttpResponseBadRequest("No seats selected.")

    seats_to_book = Seat.objects.select_for_update().filter(id__in=seat_ids, is_booked=False)
    if not seats_to_book.exists():
        return HttpResponseBadRequest("Selected seats are already booked or invalid.")
    bus = get_object_or_404(Bus, id=bus_id)
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return HttpResponseBadRequest("User not found. Please log in again.")
    booking = Booking.objects.create(bus=bus, user=user)
    booking.seats.set(seats_to_book)
    for seat in seats_to_book:
        seat.is_booked = True
        seat.save()
    seat_numbers = [seat.seat_number for seat in seats_to_book]
    total_price = float(bus.price) * len(seat_numbers)
    if user and user.email:
        subject = '🚌 Your Bus Booking is Confirmed!'
        message = (
            f"Hello {user.username},\n\n"
            f"Thank you for booking with us. Here are your ticket details:\n\n"
            f"🚌 Bus: {bus.operator}\n"
            f"📍 From: {bus.source} → To: {bus.destination}\n"
            f"⏰ Departure: {bus.departure_time}\n"
            f"💺 Seats: {', '.join(seat_numbers)}\n"
            f"💰 Total: ₹{total_price}\n\n"
            f"We wish you a safe and pleasant journey.\n\n"
            f"Regards,\nBus Booking Team"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    return render(request, 'payment.html', {
        'booked_seats': seat_numbers
    })
#@login_required
def available_tours(request):
    query = request.GET.get('q', '')
    context = {'query': query}

    if query:
        tours = Tour.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
        context['tours'] = tours  
    else:
        most_visited = Tour.objects.filter(most_visited=True)[:6]
        context['most_visited'] = most_visited
        context['tours'] = most_visited  


    return render(request, 'TourPackages.html', context)

#@login_required
def tour_list(request):
    query = request.GET.get('q')  
    if query:
        tours = Tour.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
    else:
        tours = None
    most_visited = Tour.objects.all()[:6]
    return render(request, 'tour_list.html', {
        'query': query,
        'tours': tours,
        'most_visited': most_visited,
    })
def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')
        rating = request.POST.get('rating')
        messages.success(request, 'Feedback submitted successfully!')
        return redirect('contact')
    return redirect('contact')

# def logout_view(request):
#     if request.method == 'POST':
#         logout(request)
#         messages.success(request, "You have been logged out successfully.")
#         return redirect('login_view')
#     return render(request, 'logout.html')
def tour_details(request):
    return render(request, 'tourdetailslist.html')

def tour_details(request, id):
    tour = get_object_or_404(Tour, id=id)  # Fetches the tour or shows 404 if not found
    request.session['tour_id'] = tour.id
    return render(request, 'tour_details.html', {'tour': tour})
def blogDetails(request):
    return render(request, "blogDetails.html")
def logout_view(request):
    request.session.flush()  # ✅ Clears all session data
    return redirect('login_view')
def chat(request):
    return render(request, "chatbot.html")


    
#def hotel_list(request):
#    hotels = Hotel.objects.all()
#    return render(request, 'hotel_list.html', {'hotels': hotels})
#
#def hotel_detail(request, hotel_id):
#    hotel = get_object_or_404(Hotel, id=hotel_id)
#    rooms = HotelRoom.objects.filter(hotel=hotel, is_available=True)
#    return render(request, 'hotel_detail.html', {'hotel': hotel, 'rooms': rooms})
#
#@login_required
#def book_room(request, room_id):
#    room = get_object_or_404(HotelRoom, id=room_id)
#    if request.method == "POST":
#        check_in = request.POST.get('check_in')
#        check_out = request.POST.get('check_out')
#        booking = HotelBooking.objects.create(
#            user=request.user,
#            room=room,
#            check_in=check_in,
#            check_out=check_out
#        )
#        room.is_available = False
#        room.save()
#        return redirect('hotel_list')
#    return render(request, 'book_room.html', {'room': room})