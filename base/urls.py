from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rest/<str:pk>', views.rest, name='rest'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('registerConsumer/', views.registerConsumer, name='registerConsumer'),
    path('registerProvider/', views.registerProvider, name='registerProvider'),
    path('logout/', views.logoutUser, name='logout'),
    path('createRest', views.createRestaurant, name='createRest'),
    path('bookTable/<str:pk>', views.bookTable, name='bookTable'),
    path('requests/<str:pk>', views.requests, name='requests'),
    path('profile/<str:pk>', views.profile, name='profile'),
]
