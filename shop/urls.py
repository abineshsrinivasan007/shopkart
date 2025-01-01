from django.urls import path 
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login_page,name='login'),
    path('logout/',logout_page,name='logout'),
    path('collections/',collections,name='collections'),
    path('collections/<str:name>/', collectionview, name='collectionviews'),
    path('fav',fav_page,name="fav"),
    path('favviewpage',favviewpage,name="favviewpage"),
    path('addtocart',add_to_cart,name='addtocart'),
    path('cart/',cart_page,name='cart'),
    path('collections/<str:cname>/<str:pname>/', product_details, name='productdetails'),
    path('removecart/<str:cid>',remove_cart,name='remove_cart'),
    path('removefav/<str:fid>',remove_fav,name='remove_fav'),
]