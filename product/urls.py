from django.urls import path
from . import views

urlpatterns = [

    path('get/', views.getProducts, name='getProducts'),
    path('get/<str:pk>/', views.getProduct, name='getProduct'),
    path('createWishlist/', views.addtoWishList, name='createWishlist'),
    path('getWishlist/', views.getWishList, name='getWishlist'),
    path('deleteWishlist/', views.deleteWishList, name='deleteWishlist'),
    path('addtocart/', views.addtoCart, name='addtocart'),
    path('getCart/', views.getCart, name='getCart'),
    path('deleteCart/', views.deleteCart, name='deleteCart'),
    path('createHistory/', views.createHistory, name='createHistory'),
    path('getHistory/', views.getrecommenededProducts, name='getHistory'),
    path('generateImage/', views.generateImage, name='generateImage'),
    path('generateImagetoImage/', views.imageToimage, name='generateImagetoImage'),
    path('trending/', views.generatetrendingImage, name='trending'),
    path('searchInDb/', views.searchProductInDb, name='searchInDb'),
    path('searchbyLocation/', views.searchProductbyLocationAndTrends, name='searchbyLocation'),
    path('createOrder/', views.createOrder, name='createOrder'),
    path('getOrder/', views.getOrders, name='getOrder'),
    path('requestProduct/', views.requestProduct, name='requestProduct')
]