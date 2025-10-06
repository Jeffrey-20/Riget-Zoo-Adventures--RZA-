
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('user-logout', views.user_logout, name= "user-logout"),
    
    path('dashboard', views.dashboard, name="dashboard"),

    path('create-record/', views.create_record, name="create-record"),

    path('update-record/<int:pk>/', views.update_record, name="update-record"),

    path('view_record/<int:pk>/', views.view_record,name="view_record"),

    path('delete-record/<int:pk>/', views.delete_record, name="delete-record"),

    path('book-tickets/', views.book_tickets, name="book-tickets"),

    path('confirmation/<int:pk>/', views.booking_confirmation, name="booking-confirmation"),

]


