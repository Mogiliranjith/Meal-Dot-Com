from django.urls import include, path
from . import views

urlpatterns = [
  path('', views.index),
  path('signup', views.signup, name='signup'),
  path('signin', views.signin, name='signin'),
  path('open_add_restaurant', views.open_add_restaurant, name = 'open_add_restaurant'),
]
