from django.db.models import Avg
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from blog.models import (
    CustomUser, Blog, AuthorProfile, ReaderProfile, Category, SubCategory,
    Comment, Point
)

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'user_type']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class CustomUserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    current_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'password', 'current_password']

    def validate(self, attrs):
        user = self.instance
        new_password = attrs.get('password')
        current_password = attrs.get('current_password')

        if new_password:
            if not current_password:
                raise serializers.ValidationError('current password required.')
            if not user.check_password(current_password):
                raise serializers.ValidationError('current password is False.')

        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('current_password', None)
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance

class AuthorProfileSerializer(serializers.HyperlinkedModelSerializer):
    blog_count = serializers.SerializerMethodField()

    def get_blog_count(self, obj):
        return obj.author_blogs.count()

    class Meta:
        model = AuthorProfile
        fields = '__all__'

class ReaderProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReaderProfile
        fields = '__all__'

class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    category_sub_categories = SubCategorySerializer(many=True, read_only=True)

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    blog = serializers.HyperlinkedRelatedField(
        queryset=Blog.objects.all(),
        view_name='blog-detail'
    )
    comment_parent = serializers.HyperlinkedRelatedField(
        queryset=Comment.objects.all(),
        view_name='comment-detail',
        required=False,
        allow_null=True
    )
    commenter = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='customuser-detail'
    )

    class Meta:
        model = Comment
        fields = '__all__'

class PointSerializer(serializers.HyperlinkedModelSerializer):
    blog = serializers.HyperlinkedRelatedField(
        queryset=Blog.objects.all(),
        view_name='blog-detail'
    )
    pointer = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='customuser-detail'
    )

    class Meta:
        model = Point
        fields = '__all__'

class BlogListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class BlogDetailSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        queryset=AuthorProfile.objects.all(),
        view_name='authorprofile-detail'
    )
    sub_categories = serializers.HyperlinkedRelatedField(
        queryset=SubCategory.objects.all(),
        many=True,
        view_name='subcategory-detail'
    )
    blog_comments = CommentSerializer(many=True, read_only=True)
    blog_points = PointSerializer(many=True, read_only=True)

    comment_count = serializers.SerializerMethodField()
    point_average = serializers.SerializerMethodField()
    point_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'url', 'id', 'author', 'sub_categories', 'cover_image', 'title', 'slug',
            'body', 'created_at', 'updated_at', 'status',
            'blog_comments', 'blog_points',
            'comment_count', 'point_count', 'point_average'
        ]

    def get_comment_count(self, obj):
        return obj.blog_comments.count()

    def get_point_count(self, obj):
        return obj.blog_points.count()

    def get_point_average(self, obj):
        avg = obj.blog_points.aggregate(avg_star=Avg('star'))['avg_star']
        return round(avg, 2) if avg else None

class AuthorProfileRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    blog_count = serializers.SerializerMethodField()

    def get_blog_count(self, obj):
        return obj.author_blogs.count()
    
    author_blogs = BlogListSerializer(many=True, read_only=True)

    class Meta:
        model = AuthorProfile
        fields = ['url', 'id', 'user', 'profile_image', 'country', 'phone_number', 'status', 'blog_count', 'author_blogs']