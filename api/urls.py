from django.urls import path, re_path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    CustomUserViewSet, BlogViewSet, AuthorProfileViewSet, ReaderProfileViewSet,
    CategoryViewSet, SubCategoryViewSet, CommentViewSet, PointViewSet, RegisterView, MeView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Blog Project Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your@email.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # اگه می‌خوای فقط لاگین شده‌ها ببینن بذار False
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'authorprofiles', AuthorProfileViewSet)
router.register(r'readerprofiles', ReaderProfileViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'points', PointViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]