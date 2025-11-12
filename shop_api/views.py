from pprint import pprint
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import ProductSerializer

from shop.models import Product


# Create your views here.

@api_view(['GET'])
def test_api(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    return Response({
        'id': product.id,
        'name': product.name,
        'price': product.price,
    })

@api_view(['GET'])
def test_api(request):
    products = Product.objects.all()
    category = request.query_params.get('category')
    if category:
        products = products.filter(category_id=category)
    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        } for product in products
    ]
    return Response(data)


class ProductDetailAPIView(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        return Response({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'price_with_vat': product.price_with_vat
        })


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCreateAPIView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)  # десериализация входных данных
        if serializer.is_valid():  # проверка данных
            serializer.save()  # создание нового объекта Product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        pprint(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def set_cookie_example(request):
    response = Response({'message': 'Cookie установлено'})
    response.set_cookie(
        key='user_token',
        value='12345abcdef',
        max_age=15,  # 1 час
        httponly=True  # запрещает доступ к cookie из JS
    )
    return response


@api_view(['GET'])
def get_cookie_example(request):
    token = request.COOKIES.get('user_token')
    if token:
        return Response({'message': 'Cookie найден', 'token': token})
    return Response({'message': 'Cookie не найден'}, status=404)
