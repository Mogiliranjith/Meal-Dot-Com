from django.urls import include, path
from . import views

urlpatterns = [
  path('', views.index),
  path('signup', views.signup, name='signup'),
  path('signin', views.signin, name='signin'),
  path('open_add_restaurant', views.open_add_restaurant, name = 'open_add_restaurant'),
  path('add_restaurant', views.add_restaurant, name="add_restaurant"),
  path('open_show_restaurant', views.open_show_restaurant, name="open_show_restaurant"),
]
