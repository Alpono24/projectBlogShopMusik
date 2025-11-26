from pprint import pprint

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from blog.models import Post

from blog_api.serializers import PostSerializer
from shop_api.serializers import RegisterSerializer


# Create your views here.


class BlogListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Информация по статьям из блога",
        operation_description="Получение информации по статьям из блога",
        responses={
            200: 'It is very good',
                },
    )
    def get(self, request):
        posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="О статье из блога",
        operation_description="Получение информации о статье из блога",
        responses={
            200: 'Статья найдена и передана успешно',
            400: 'Некорректный запрос',
            401: 'Вы не аутентифицированы. Доступ запрещен.',
            403: 'Данная статья не найдена.',
            404: 'Статьи с указанным идентификатором не существует.',
            500: 'Внутренняя ошибка сервера',
        },
    )
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

        return Response({
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'author': str(post.author),
            'category': str(post.category) if post.category else '',
            'created_at': post.created_at.isoformat(),
        }, status=status.HTTP_200_OK)


class PostCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Создать статью",
        operation_description="Создание новой статьи для блога",
        request_body=PostSerializer,
        responses={
            200: 'Статья создана успешно',
            201: 'Запрос был успешно выполнен',
            400: 'Некорректный запрос',
            401: 'Вы не аутентифицированы. Доступ запрещен.',
            403: 'Данная статья не найдена.',
            404: 'Статьи с указанным идентификатором не существует.',
            500: 'Внутренняя ошибка сервера',
                },
    )
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)