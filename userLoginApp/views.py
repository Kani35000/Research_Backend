from django.shortcuts import render
from .models import User

# Create your views here.
def home(request):
    user = User.objects
    return render(request, 'userLoginApp/home.html',{'user':user})