from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tour,Bus, Seat,Booking,TravelPackage
from Tourism import settings
from django.core.mail import send_mail
from .models import CustomUser
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
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
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                # You can implement session login manually here if needed
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                error = "Invalid username or password"
        except CustomUser.DoesNotExist:
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
        elif CustomUser.objects.filter(username=username).exists():
            error = "Username already exists"
        elif CustomUser.objects.filter(email=email).exists():
            error = "Email already in use"
        else:
            hashed_password = make_password(password1)
            CustomUser.objects.create(username=username, email=email, password=hashed_password)
            return redirect('login_view')

    return render(request, 'register.html', {'error': error})

def forgot_password(request):
    message = error = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            reset_link = f"http://127.0.0.1:8000/reset-password/{user.id}/"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'your_email@gmail.com',  
                [email],
                fail_silently=False,
            )
            message = 'Password reset link sent to your email.'
        else:
            error = 'Email not found.'
    return render(request, 'forgot_password.html', {'message': message, 'error': error})


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

def bus_list(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')

    if source and destination:
        buses = Bus.objects.filter(source__icontains=source, destination__icontains=destination)
    else:
        buses = Bus.objects.all()
        
    return render(request, 'bus_list.html', {'buses': buses})



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


def payment_form(request):
    bus_id = request.session.get('bus_id')
    seat_ids = request.session.get('selected_seat_ids', [])
    
    if not bus_id or not seat_ids:
        return HttpResponseBadRequest("Missing bus or seat info.")
    bus = get_object_or_404(Bus, id=bus_id)
    seats = Seat.objects.filter(id__in=seat_ids)
    total_price = float(bus.price) * len(seats)

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

def available_tours(request):
    query = request.GET.get('q', '')
    context = {'query': query}

    if query:
        tours = Tour.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
        context['tours'] = tours  
    else:
        most_visited = Tour.objects.filter(most_visited=True)[:6]   
        context['most_visited'] = most_visited
        most_visited = Tour.objects.filter(most_visited=True)[:6]
        context['most_visited'] = most_visited  


    return render(request, 'TourPackages.html', context)


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
