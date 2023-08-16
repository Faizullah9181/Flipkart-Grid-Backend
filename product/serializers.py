from .models import Product, ProductInventory,Category,Cart,WishList
from user.models import Users
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug','type')

class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ('id','productId','size','price')


class ProductSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id','name','description','gender','categoryId','color','image','inventory')

    
    def get_inventory(self, obj):
        inventory = ProductInventory.objects.filter(productId=obj.id)
        return ProductInventorySerializer(inventory, many=True).data
    

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id','created_by','size','quantity','total_price','product')


class ProductSerializerForWC(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','description','gender','categoryId','color','image')
    

class WishListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = WishList
        fields = ('id','created_by','productInventoryId','product')

    def get_product(self, obj):
        product = Product.objects.filter(id=obj.productInventoryId.productId.id)
        return ProductSerializerForWC(product, many=True).data