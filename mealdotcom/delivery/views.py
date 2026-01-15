from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Q

from .models import Cart, User, Restaurant, Item
import razorpay


# Create your views here.
def index(request):
  return render(request, "delivery/index.html")

# Signup logic
def signup(request):
  if request.method != 'POST':
    return HttpResponse("Invalid Request")
  
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

# Signin method
def signin(request):
  if request.method != "POST":
    return HttpResponse("Invalid Request")
  
  email = request.POST.get("email")
  password = request.POST.get("password")

  user = User.objects.filter(email = email, password = password).first()

  if not user:
    return render(
      request,
      "delivery/index.html",
      {"error": "Invalid email or password", "show": "signin"}
    )
  
  # Admin login
  if user.email == "admin@gmail.com":
    return admin_home(request)
  
  # Customer login
  restaurants = Restaurant.objects.all()
  return render(
    request,
    "delivery/customer_home.html",
    {
      "restaurantList": restaurants,
      "name": user.name
    }
  )

#adding restaurants
def add_restaurant(request):
  if request.method != 'POST':
    return HttpResponse("Invalid Request")
  
  name = request.POST.get('name')
  picture = request.POST.get('picture')
  cuisine = request.POST.get('cuisine')
  address = request.POST.get('address')
  location = request.POST.get('location')
  rating = request.POST.get('rating')

  if not picture:
    picture = '/static/delivery/images/default.jpg'

  #check for duplicate by name + address
  if Restaurant.objects.filter(name = name, address = address).exists():
    messages.error(request, "Restaurant already exists.")
    return redirect('admin_home')
    
  Restaurant.objects.create(
    name = name,
    picture = picture,
    cuisine = cuisine,
    address = address,
    location = location,
    rating = rating,
  )
  messages.success(request, "Restaurant added successfully.")
  return redirect('admin_home')

def admin_home(request):
  restaurantList = Restaurant.objects.all()
  return render(
    request, "delivery/admin_home.html",
    {
      "restaurantList": restaurantList
    }
  )

#opening update menu html
def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, "delivery/update_menu.html",{"itemList" : itemList, "restaurant" : restaurant})

# item adding functionality
def update_menu(request, restaurant_id):
  restaurant = get_object_or_404(Restaurant, id=restaurant_id)

  if request.method == 'POST':
      name = request.POST.get('name')
      description = request.POST.get('description')
      price = request.POST.get('price')
      vegeterian = request.POST.get('vegeterian') == 'on'
      picture = request.POST.get('picture')

      if not picture:
        picture = 'static/delivery/images/default.jpg'

      if Item.objects.filter(name=name, restaurant=restaurant).exists():
          return HttpResponse("Duplicate item for this restaurant!")

      Item.objects.create(
          restaurant=restaurant,
          name=name,
          description=description,
          price=price,
          vegeterian=vegeterian,
          picture=picture,
      )

      return redirect('open_update_menu', restaurant_id=restaurant.id)

  return HttpResponse("Invalid Request")

# Deleting a menu item
def delete_menu_item(request, item_id):
  if request.method != "POST":
      return HttpResponse("Invalid Request")

  item = get_object_or_404(Item, id=item_id)
  restaurant_id = item.restaurant.id
  item.delete()

  return redirect('open_update_menu', restaurant_id=restaurant_id)


# clicking on the update restaurant button
# def update_restaurant(request, restaurant_id):
#   restaurant = Restaurant.objects.get(id = restaurant_id)
#   if request.method == 'POST':
#     name = request.POST.get('name')
#     picture = request.POST.get('picture')
#     cuisine = request.POST.get('cuisine')
#     rating = request.POST.get('rating')

#     if not picture:
#       picture = 'static/delivery/images/default.jpg'

#     restaurant.name = name
#     restaurant.picture = picture
#     restaurant.cuisine = cuisine
#     restaurant.rating = rating

#     restaurant.save()
  
#   restaurantList = Restaurant.objects.all()
#   return render(request, 'delivery/admin_home.html', {"restaurantList"})

# clicking on the update restaurant button inside the open_update_restaurant.html
def update_restaurant(request, restaurant_id):
  restaurant = Restaurant.objects.get(id = restaurant_id)
  if request.method != 'POST':
    return HttpResponse("Invalid Request")
  
  name = request.POST.get('name')
  picture = request.POST.get('picture')
  cuisine = request.POST.get('cuisine')
  rating = request.POST.get('rating')

  if not picture:
    picture = '/static/delivery/images/default.jpg'
    
  restaurant.name = name
  restaurant.picture = picture
  restaurant.cuisine = cuisine
  restaurant.rating = rating

  restaurant.save()
  
  restaurantList = Restaurant.objects.all()

  messages.success(request, "Restaurant added successfully.")
  return redirect('admin_restaurant_detail', restaurant_id = restaurant.id)

# Clicking on the delete restaurant button inside admin_home.html
def delete_restaurant(request, restaurant_id):
  restaurant = Restaurant.objects.get(id = restaurant_id)
  restaurant.delete()

  restaurantList = Restaurant.objects.all()
  return render(request, 'delivery/admin_home.html', {"restaurantList": restaurantList})

# Viewing a particular restaurant
def admin_restaurant_detail(request, restaurant_id):
  restaurant = get_object_or_404(Restaurant, id = restaurant_id)
  itemList = restaurant.items.all()

  return render(
    request,
    "delivery/admin_restaurant_detail.html",
    {
      "restaurant": restaurant,
      "itemList": itemList
    }
  )



# CUSTOMER SPECIFIC
#Customer view menu 
def view_menu(request, restaurant_id, name):
  restaurant = Restaurant.objects.get(id = restaurant_id)
  itemList = restaurant.items.all()
  #return HttpResponse("Items collected")
  #itemList = Item.objects.all()
  return render(request, 'delivery/customer_menu.html',
                {"itemList" : itemList,
                  "restaurant" : restaurant, 
                  "name":name})

# add to cart show
def add_to_cart(request, item_id, name):
  item = Item.objects.get(id = item_id)
  customer = User.objects.get(name = name)
  cart, created = Cart.objects.get_or_create(customer = customer)
  cart.items.add(item)
  return HttpResponse('added to cart')

# show cart functionality
def show_cart(request, name):
  customer = User.objects.get(name = name)
  cart = Cart.objects.filter(customer=customer).first()
  items = cart.items.all() if cart else []
  total_price = cart.total_price() if cart else 0
  return render(request, 'delivery/cart.html',{"itemList" : items, "total_price" : total_price, "name":name})

# check out functionality
def checkout(request, name):
  customer = get_object_or_404(User, name = name)
  cart = Cart.objects.filter(customer = customer).first()
  cart_items = cart.items.all() if cart else []
  total_price = cart.total_price() if cart else 0
  
  if total_price == 0:
    return render(request, 'delivery/checkout.html', {
      'error': 'Your cart is empty!',
    })
  #Initialize Razorpay client
  client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
  
  #Create Razorpay order
  order_data = {
    'amount': int(total_price * 100), # Amount in paisa
    'currency': 'INR',
    'payment_capture': '1', # Automatically capture payment
  }
  order = client.order.create(data = order_data)
  
  #Pass the order details to the frontend
  return render(request, 'delivery/checkout.html', {
    'name': name,
    'cart_items': cart_items,
    'total_price': total_price,
    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    'order_id': order['id'], # Razorpay order ID
    'amount': total_price,
  })

# recent orders
def orders(request, name):
  customer = get_object_or_404(User, name = name)
  cart = Cart.objects.filter(customer=customer).first()
  
  # Fetch cart items and total price before clearing the cart
  cart_items = cart.items.all() if cart else[]
  total_price = cart.total_price() if cart else 0
  
  # Clear the cart after fetching its details
  if cart:
    cart.items.clear()
    
  return render(request, 'delivery/orders.html', {
    'name': name,
    'customer': customer,
    'cart_items': cart_items,
    'total_price': total_price,
  })
  


# FEATURES
# home page search functionality
def live_search(request):
  query = request.GET.get('q', '').strip()

  if not query:
    restaurants = Restaurant.objects.all()
  else:
    restaurants = Restaurant.objects.filter(
      Q(name__icontains=query) |
      Q(items__name__icontains=query)
    ).distinct()

  data = []
  for r in restaurants:
      data.append({
        'id': r.id,
        'name': r.name,
        'cuisine': r.cuisine,
        'rating': r.rating,
        'picture': r.picture if r.picture else '/static/delivery/images/default.jpg'
      })

  return JsonResponse({'results': data})

# menu page search funtionality
def menu_live_search(request):
  query = request.GET.get('q', '').strip()
  restaurant_id = request.GET.get('restaurant_id')

  items = Item.objects.filter(restaurant_id=restaurant_id)

  if query:
    items = items.filter(name__icontains=query)

  data = []
  for item in items:
      data.append({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'vegeterian': item.vegeterian,
        'picture': item.picture if item.picture else '/static/delivery/images/default.jpg'
      })

  return JsonResponse({'results': data})
