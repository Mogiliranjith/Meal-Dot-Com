from django.urls import include, path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('signup', views.signup, name='signup'),
  path('signin', views.signin, name='signin'),

  # Admin Specific
  path('admin_home', views.admin_home, name='admin_home'),
  path('add_restaurant', views.add_restaurant, name="add_restaurant"),
  path('open_update_menu/<int:restaurant_id>', views.open_update_menu, name='open_update_menu'),
  path('update_menu/<int:restaurant_id>', views.update_menu, name='update_menu'),
  path('delete_menu_item/<int:item_id>', views.delete_menu_item, name='delete_menu_item'),
  path('update_restaurant/<int:restaurant_id>', views.update_restaurant, name='update_restaurant'),
  path('delete_restaurant/<int:restaurant_id>', views.delete_restaurant, name='delete_restaurant'),
  path('admin_restaurant_detail/<int:restaurant_id>/', views.admin_restaurant_detail, name='admin_restaurant_detail'),

  # Customer Specific
  path('view_menu/<int:restaurant_id>/<str:name>', views.view_menu, name='view_menu'),
  path('add_to_cart/<int:item_id>/<str:name>', views.add_to_cart, name='add_to_cart'),
  path('show_cart/<str:name>', views.show_cart, name='show_cart'),
  path('checkout/<str:name>/', views.checkout, name='checkout'),
  path('orders/<str:name>/', views.orders, name='orders'),
  path('customer_profile/', views.customer_profile, name='customer_profile'),
  path('customer_logout/', views.customer_logout, name='customer_logout'),
  
  # Features
  path('live-search/', views.live_search, name='live_search'),
  path('menu-live-search/', views.menu_live_search, name='menu_live_search'),
  path("my-orders/", views.order_history_page, name="order_history_page"),

]
