from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('books/',views.view_book,name="books"),

    path('show_book/<str:pk>/',views.show_book,name="show_book"),
    path('cart/<str:pk>/',views._cart_,name="cart"),
    path('show_my_cart/',views.show_cart,name="show_cart"),
    path('login/',views.userlogin,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.userregister,name="register"),

    path('view_order/',views.view_order,name="view_order"),
    path('update_cart/<str:pk>/',views.update_cart,name="update_cart"),
    path('show_library/',views.view_book_lib,name="show_library"),
    #admin url
    path('adminbw/',views.view_admin,name="adminbw"),
    path('adminbw/<str:pk>/',views.book_data_admin,name="book_data_admin"),
    path('adminbw_books/',views.admin_books,name="admin_books"),
    path('adminbw_create_books/',views.admin_create_books,name="admin_create_books"),

    path('adminbw_books_update/<str:pk>/',views.admin_books_update,name="admin_books_update"),
    path('adminbw_author/',views.admin_author,name="admin_author"),
    path('adminbw_create_author/',views.admin_create_author,name="admin_create_author"),
    
    path('adminbw_author_update/<str:pk>/',views.admin_author_update,name="admin_author_update"),
]
