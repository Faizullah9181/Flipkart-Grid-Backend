import re
from .serializers import ProductSerializer, CartSerializer, WishListSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Cart, WishList, UserHistory, Order, RequestedProducts
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .imagegenration import get_image, get_image_from_image
from .utils import strUtiltext, strUtilimage, get_details
from django.db.models import Q
from functools import reduce
import operator
import random


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all().order_by('?')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    product_name = product.name
    product_name = product_name.split(' ')
    product_query = reduce(operator.or_, (Q(name__icontains=item) for item in product_name))
    products = Product.objects.filter(product_query).exclude(id=pk).order_by('-created_at')
    serializer = ProductSerializer(product, many=False)
    similar_products = ProductSerializer(products, many=True)
    return Response({'product': serializer.data, 'similar_products': similar_products.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtoWishList(request):
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    if (WishList.objects.filter(productId=product, created_by=request.user).exists()):
        return Response('Product Already in WishList', status=status.HTTP_400_BAD_REQUEST)
    wishlist = WishList.objects.create(
        created_by=request.user,
        productId=product
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
    product_id = data['product_id']
    quantity = data['quantity']
    product = Product.objects.get(id=product_id)
    if (Cart.objects.filter(productId=product, created_by=request.user).exists()):
        return Response('Product Already in Cart', status=status.HTTP_400_BAD_REQUEST)
    cart = Cart.objects.create(
        created_by=request.user,
        productId=product,
        quantity=quantity,
        total_price=product.price * quantity
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
    color = prompt.split(' ')[0]
    product_description = strUtiltext(
        'generate more details about this ' + prompt + ' only 50 words description')
    product_description = product_description['content']
    product_description = product_description[1]
    product_name = strUtiltext(
        'Generate a unique and catchy product title ' + prompt + ' only in 10 words')
    product_name_words = product_name['content'][1]
    product_name_words = product_name_words.split(',')[0].split('.')[0]
    product_name_words = product_name_words.split(' ')
    product_name_words = product_name_words[:15]
    product_name_words = ' '.join(product_name_words)
    product_gender = strUtiltext(
        'gender of this product' + prompt + 'in one word please dont send any other information only send response in men or women i want only one word response')

    product_gender = strUtiltext(
        'give gender of this product in one word')

    gender_content = product_gender['content'][0].lower()
    if 'women' in gender_content:
        gender = 'women'
    elif 'men' in gender_content:
        gender = 'men'
    image_data = strUtilimage('generate ' + prompt + ' 10 images')
    image_data = image_data['images']
    product_ids = []
    for image in image_data:
        product = Product.objects.create(
            name=product_name_words,
            description=product_description,
            price=random.randint(1000, 2000),
            color=color,
            brand=random.choice(['Flipkart', 'Myntra', 'Amazon', 'Ajio']),
            image=image,
            gender=gender
        )
        product_ids.append(product.id)
        product.save()
    product_db_name = Product.objects.filter(name__icontains=prompt)
    product_db_description = Product.objects.filter(
        description__icontains=prompt)
    product_db = list(set(list(product_db_name) +
                      list(product_db_description)))
    product_db = product_db[:4]
    print("a", product_db)
    products = Product.objects.filter(id__in=product_ids)
    products = products[:8]
    print("b", products)
    products = list(set(list(products) + list(product_db)))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchProductInDb(request):
    cart_product_ids = Cart.objects.filter(
        created_by=request.user).values_list('productId', flat=True)
    wishlist_product_ids = WishList.objects.filter(
        created_by=request.user).values_list('productId', flat=True)
    user_history_product_ids = UserHistory.objects.filter(
        created_by=request.user).values_list('productId', flat=True)
    order_history_product_ids = Order.objects.filter(
        created_by=request.user).values_list('productId', flat=True)
    product_ids = list(set(list(cart_product_ids) +
                           list(wishlist_product_ids) + list(user_history_product_ids) + list(order_history_product_ids)))

    products = Product.objects.filter(id__in=product_ids)
    if (len(products) == 0):
        return Response('Sorry No Products Found', status=status.HTTP_400_BAD_REQUEST
                        )
    p_names = []
    p_descriptions = []
    for product in products:
        p_names.append(product.name)
        p_descriptions.append(product.description)
    p_names = [x for xs in p_names for x in xs.split()]
    name_queries = [Q(name__icontains=x) for x in p_names]
    description_queries = [Q(description__icontains=x) for x in p_descriptions]
    name_query = reduce(operator.or_, name_queries)
    description_query = reduce(operator.or_, description_queries)
    products = Product.objects.filter(
        name_query | description_query).exclude(id__in=product_ids)
    products = sorted(products, key=lambda x: x.created_at, reverse=True)
    random.shuffle(products)
    products = products[:12]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def searchProductbyLocationAndTrends(request):
    user = request.user
    location = user.address
    get_trends = get_details("Give me a list of popular fashion trends on instagram in " +
                             location + " as a list. Give only the name of the trends.","bai")
    get_trends = get_trends.replace('\n', ', ')
    get_trends = get_trends.split('.')

    cleaned_data = [re.sub(r'[^a-zA-Z ]+', '', item) for item in get_trends]
    cleaned_data = [re.sub(r'n$', '', re.sub(r'[^a-zA-Z ]+', '', item))
                    for item in get_trends]
    split_words = []
    for style in cleaned_data:
        split_words.extend(style.split())

    cleaned_data = [item for item in split_words if item]
    product_query = reduce(
        operator.or_, [Q(name__icontains=x) for x in cleaned_data])

    product = Product.objects.filter(product_query)
    if product:
        product = list(product)
        random.shuffle(product)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    else:
        return Response("No product found")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(id=product_id)
    order = Order.objects.create(
        productId=product,
        created_by=request.user,
        total_price=product.price
    )
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrders(request):
    orders = Order.objects.filter(created_by=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def requestProduct(request):
    data = request.data
    product_image = data['product_image']
    request_product = RequestedProducts.objects.create(
        productimage=product_image,
        created_by=request.user
    )
    request_product.save()
    return Response('Request Sent')
