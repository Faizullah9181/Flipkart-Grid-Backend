from .serializers import CategorySerializer, ProductSerializer,ProductInventorySerializer,CartSerializer,WishListSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, ProductInventory,Cart ,WishList
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response



@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all().order_by('-created_at')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtoWishList(request):
    data = request.data
    product_inventory_id = data['product_inventory_id']
    product_inventory = ProductInventory.objects.get(id=product_inventory_id)
    if(WishList.objects.filter(productInventoryId=product_inventory,created_by=request.user).exists()):
        return Response('Product Already in WishList'
        ,status=status.HTTP_400_BAD_REQUEST)
    wishlist = WishList.objects.create(
        created_by=request.user,
        productInventoryId = product_inventory
    )
    serializer = WishListSerializer(wishlist, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getWishList(request):
    wishlist = WishList.objects.filter(created_by=request.user)
    serializer = WishListSerializer(wishlist, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteWishList(request):
    data = request.data
    wishlist_id = data['wishlist_id']
    if(WishList.objects.filter(id=wishlist_id,created_by=request.user).exists() == False):
        return Response('WishList Item Not Found'
        ,status=status.HTTP_400_BAD_REQUEST
        )
    wishlist = WishList.objects.get(id=wishlist_id)
    wishlist.delete()
    return Response('WishList Item Removed')



