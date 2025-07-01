from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # features
    path('requests/', views.request_list, name='request_list'),
    path('offers/', views.offer_list, name='offer_list'),
    path('requests/new/', views.create_request, name='create_request'),
    path('offers/new/', views.create_offer, name='create_offer'),
    path('categories/new/', views.add_category, name='add_category'),
    path('requests/<int:request_id>/offer_help/', views.offer_help, name='offer_help'),
    path('requests/delete/<int:request_id>/', views.delete_request, name='delete_request'),


]
