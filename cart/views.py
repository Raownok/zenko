from django.shortcuts import render
from . import models
from django.core.paginator import Paginator

# Create your views here.
   
def cart_Summary(request):

    return render(request,'cart.html',{})

