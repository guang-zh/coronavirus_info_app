#polls/views.py
# render the html page that is stored in templates
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse('<h2 style="background:blue; color:white;width:50%;"> our first view </h2>')

def home(request):
    return render (request, 'polls/home.html')

def contact(request):
    return render (request, 'polls/contact.html')