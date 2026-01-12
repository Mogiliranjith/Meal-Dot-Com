from django.urls import include, path
from . import views

urlpatterns = [
  path('', views.index),
  path('signup', views.signup, name='signup'),
  path('signin', views.signin, name='signin'),
  path('admin_home', views.admin_home, name='admin_home'),
  path('open_add_restaurant', views.open_add_restaurant, name = 'open_add_restaurant'),
  path('add_restaurant', views.add_restaurant, name="add_restaurant"),
  path('open_update_menu/<int:restaurant_id>', views.open_update_menu, name='open_update_menu'),
  path('update_menu/<int:restaurant_id>', views.update_menu, name='update_menu'),
  path('delete_menu_item/<int:item_id>', views.delete_menu_item, name='delete_menu_item'),
  path('view_menu/<int:restaurant_id>/<str:name>', views.view_menu, name='view_menu'),
  path('add_to_cart/<int:item_id>/<str:name>', views.add_to_cart, name='add_to_cart'), 
]
