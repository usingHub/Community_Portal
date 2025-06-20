from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('requests/', views.request_list, name='request_list'),
    path('offers/', views.offer_list, name='offer_list'),
    path('requests/new/', views.create_request, name='create_request'),
    path('offers/new/', views.create_offer, name='create_offer'),
]
