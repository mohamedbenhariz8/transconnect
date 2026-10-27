from django.shortcuts import render
from django.http import HttpResponse 
from .models import expedition

# Create your views here.
def home(request):
    return HttpResponse("<h1>welcome to the Expeditions App</h1>")
def welcome(request,name):
    return HttpResponse(f"<h1>Welcome {name} to the Expeditions App</h1>")
def listExpeditions(request):
    list=expedition.objects.all()
    return render(request,'expedition/list.html',{"liste":list})
def detailExpedition(request,pk):
    exp=expedition.objects.get(pk=pk)
    return render(request,'expedition/detail.html',{"exp":exp})    


    
    
    