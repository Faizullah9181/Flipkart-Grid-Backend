from .models import Product,Cart,WishList,UserHistory,Order,RequestedProducts
from user.models import Users
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','description','gender','color','image','price','brand')

    
    

class ProductSerializerForWC(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','description','gender','color','image','price','brand')
    

class WishListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = WishList
        fields = ('id','created_by','product')

    def get_product(self, obj):
        product = Product.objects.filter(id=obj.productId.id)
        return ProductSerializerForWC(product, many=True).data
    


class CartSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ('id','created_by','quantity','total_price','product')


    def get_product(self, obj):
        product = Product.objects.filter(id=obj.productId.id)
        return ProductSerializerForWC(product, many=True).data
    

class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id','created_by','product')


    def get_product(self, obj):
        product = Product.objects.filter(id=obj.productId.id)
        return ProductSerializerForWC(product, many=True).data