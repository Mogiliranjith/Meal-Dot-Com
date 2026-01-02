from django.shortcuts import render
from django.http import HttpResponse
from.models import User, Restaurant

# Create your views here.
def index(request):
  return render(request, "delivery/index.html")

def signup(request):
  if request.method == 'POST':
    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    phone = request.POST.get("phone")

    if User.objects.filter(email = email).exists():
      return render(
        request,
        "delivery/index.html",
        {
          "error": "This email is already registered.",
          "show": "signup"
        }
      )
      
    # user = User(name = name, password = password, email = email, phone = phone)
    # user.save()

    #this is the shortcut to store the user details into the django db
    User.objects.create(
      name = name,
      email = email,
      password = password,
      phone = phone
    )
    
    return render(
      request,
      "delivery/index.html",
      {
        "success": "Registration successful. Please sign in.",
        "show": "signin"
      }
    )
  else:
    return HttpResponse("Invalid Response")

#Signin.... method
def signin(request):
  if request.method == 'POST':
    email = request.POST.get('email', "").strip()
    password = request.POST.get('password', "").strip()

    user = User.objects.filter(email = email, password = password).first()

    if user:
      return HttpResponse("Signin successful")
    
    return render(
      request,
      "delivery/index.html",
      {
        "error": "Invalid email or password",
        "show": "signin"
      }
    )
  return HttpResponse("Invalid Request")

#Checking for admin login and displaying the pages accordingly
def signin(request):
  if request.method == "POST":
    email = request.POST.get('email')
    password = request.POST.get('password')
  
  try:
    User.objects.get(email = email, password = password)
    if email == 'admin@gmail.com':
      return render(request, 'delivery/admin_home.html')
    else:
      return render(request, 'delivery/customer_home.html')
    
  except User.DoesNotExist:
    return HttpResponse("User does not exist.")
  
#opening add restaurants for the admin
def open_add_restaurant(request):
  return render(request, 'delivery/add_restaurant.html')

#adding restaurants
def add_restaurant(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    picture = request.POST.get('picture')
    cuisine = request.POST.get('cuisine')
    address = request.POST.get('address')
    rating = request.POST.get('rating')

    #check for duplicate by name + address
    if Restaurant.objects.filter(name = name, address = address).exists():
      return HttpResponse("Duplicate restaurant!")
    
    Restaurant.objects.create(
      name = name,
      picture = picture,
      cuisine = cuisine,
      address = address,
      rating = rating,
    )
    return HttpResponse("Successfully Added !")
    #return render(request, 'admin_home.html')