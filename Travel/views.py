from django.shortcuts import render
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'Contacts.html')
# Create your views here.
