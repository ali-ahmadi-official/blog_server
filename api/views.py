from rest_framework import viewsets, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import (
    CustomUser, Blog, AuthorProfile, ReaderProfile, Category, SubCategory,
    Comment, Point
)
from .serializers import (
    CustomUserSerializer, RegisterSerializer, CustomUserUpdateSerializer,
    BlogListSerializer, BlogDetailSerializer, 
    AuthorProfileSerializer, AuthorProfileRetrieveSerializer, ReaderProfileSerializer,
    CategorySerializer, SubCategorySerializer,
    CommentSerializer, PointSerializer
)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'update':
            return CustomUserUpdateSerializer
        else:
            return CustomUserSerializer
        
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['user_type', 'is_superuser', 'is_staff']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id']

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

class MeView(APIView):

    def get(self, request):
        serializer = CustomUserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class AuthorProfileViewSet(viewsets.ModelViewSet):
    queryset = AuthorProfile.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuthorProfileRetrieveSerializer
        else:
            return AuthorProfileSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['country', 'status']
    search_fields = ['phone_number']
    ordering_fields = ['id']

class ReaderProfileViewSet(viewsets.ModelViewSet):
    queryset = ReaderProfile.objects.all()
    serializer_class = ReaderProfileSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogDetailSerializer
        return BlogListSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'author', 'sub_categories']
    search_fields = ['title', 'body']
    ordering_fields = ['id', 'created_at', 'updated_at']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
