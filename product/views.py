from .serializers import CategorySerializer, ProductSerializer, ProductInventorySerializer, CartSerializer, WishListSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, ProductInventory, Cart, WishList, UserHistory
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .imagegenration import get_image, get_image_from_image
from .utils import strUtiltext, strUtilimage


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
    if (WishList.objects.filter(productInventoryId=product_inventory, created_by=request.user).exists()):
        return Response('Product Already in WishList', status=status.HTTP_400_BAD_REQUEST)
    wishlist = WishList.objects.create(
        created_by=request.user,
        productInventoryId=product_inventory
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
    if (WishList.objects.filter(id=wishlist_id, created_by=request.user).exists() == False):
        return Response('WishList Item Not Found', status=status.HTTP_400_BAD_REQUEST
                        )
    wishlist = WishList.objects.get(id=wishlist_id)
    wishlist.delete()
    return Response('WishList Item Removed')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtoCart(request):
    data = request.data
    product_inventory_id = data['product_inventory_id']
    quantity = data['quantity']
    product_inventory = ProductInventory.objects.get(id=product_inventory_id)
    if (Cart.objects.filter(productInventoryId=product_inventory, created_by=request.user).exists()):
        return Response('Product Already in Cart', status=status.HTTP_400_BAD_REQUEST)
    cart = Cart.objects.create(
        created_by=request.user,
        productInventoryId=product_inventory,
        quantity=quantity,
        total_price=product_inventory.price * quantity
    )
    serializer = CartSerializer(cart, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCart(request):
    cart = Cart.objects.filter(created_by=request.user)
    serializer = CartSerializer(cart, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteCart(request):
    data = request.data
    cart_id = data['cart_id']
    if (Cart.objects.filter(id=cart_id, created_by=request.user).exists() == False):
        return Response('Cart Item Not Found', status=status.HTTP_400_BAD_REQUEST
                        )
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return Response('Cart Item Removed')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createHistory(request):
    data = request.data
    product_id = data['product_id']
    data = data['data']
    if (UserHistory.objects.filter(productId=product_id, created_by=request.user).exists()):
        return Response('Something Went Wrong', status=status.HTTP_400_BAD_REQUEST
                        )
    product = Product.objects.get(id=product_id)
    history = UserHistory.objects.create(
        created_by=request.user,
        productId=product,
        data=data
    )
    return Response('History Created')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getrecommenededProducts(request):
    productIds = UserHistory.objects.filter(
        created_by=request.user).values_list('productId', flat=True)
    products = Product.objects.filter(id__in=productIds)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def generateImage(request):
    data = request.data
    prompt = data['prompt']
    image_data = get_image(prompt)
    return Response(image_data)


@api_view(['POST'])
def imageToimage(request):
    data = request.data
    image_url = data['image_url']
    prompt = data['prompt']
    image_data = get_image_from_image(prompt, image_url)
    return Response(image_data)


@api_view(['POST'])
def generatetrendingImage(request):
    data = request.data
    prompt = data['prompt']
    product_description = strUtiltext(
        'generate more details about this ' + prompt + ' only 50 words description')
    product_name = strUtiltext(
        'generate product name for this ' + prompt + ' only 10 words name very short')
    product_name_words = product_name['content'].split()[:10]
    truncated_product_name = ' '.join(product_name_words)
    image_data = strUtilimage('generate ' + prompt + ' 10 images')
    image_data = image_data['images']
    product_ids = []
    for image in image_data:
        product = Product.objects.create(
            name=truncated_product_name,
            description=product_description['content'],
            image=image,
            categoryId=Category.objects.get(id=1)
        )
        product_ids.append(product.id)
        product.save()
    products = Product.objects.filter(id__in=product_ids)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)