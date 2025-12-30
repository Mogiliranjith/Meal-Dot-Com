from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return render(request, "delivery/index.html")

def signup(request):
  if request.method == 'POST':
    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    phone = request.POST.get("phone")
    return HttpResponse("Sign up Successful")

  else:
    return HttpResponse("Invalid Response")