from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('books/',views.view_book,name="books"),

    path('show_book/<str:pk>/',views.show_book,name="show_book"),
    path('cart/<str:pk>/',views._cart_,name="cart"),
    path('login/',views.userlogin,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.userregister,name="register"),
]
