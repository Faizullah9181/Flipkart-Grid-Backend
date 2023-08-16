from django.urls import path
from . import views

urlpatterns = [

    path('get/', views.getProducts, name='getProducts'),
    path('get/<str:pk>/', views.getProduct, name='getProduct'),
    path('getCategory/', views.getCategories, name='getCategory'),
    path('createWishlist/', views.addtoWishList, name='createWishlist'),
    path('getWishlist/', views.getWishList, name='getWishlist'),
    path('deleteWishlist/', views.deleteWishList, name='deleteWishlist'),
    path('addtocart/', views.addtoCart, name='addtocart'),
    path('getCart/', views.getCart, name='getCart'),
    path('deleteCart/', views.deleteCart, name='deleteCart')
]