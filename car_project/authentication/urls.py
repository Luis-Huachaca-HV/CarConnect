# authentication/urls.py
from django.urls import path
from . import views
from cars.urls import views as cars_views
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('',cars_views.car_list, name='cars_list'),
    # Add more authentication-related URLs as needed
]
