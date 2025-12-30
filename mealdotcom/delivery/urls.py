from django.urls import include, path
from . import views

urlpatterns = [
  path('', views.index),
  path('signup', views.signup, name='signup'),
]
