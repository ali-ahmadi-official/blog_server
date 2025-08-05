from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import CustomUser, AuthorProfile, ReaderProfile, Category, SubCategory, Blog, Comment, Point

class AuthorProfileInline(admin.StackedInline):
    model = AuthorProfile
    can_delete = False
    verbose_name_plural = 'Author Profile'
    fk_name = 'user'

class ReaderProfileInline(admin.StackedInline):
    model = ReaderProfile
    can_delete = False
    verbose_name_plural = 'Reader Profile'
    fk_name = 'user'

class BlogInline(admin.StackedInline):
    model = Blog
    fk_name = 'author'
    extra = 0

class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    fk_name = 'category'
    extra = 0

class CommentInline(admin.StackedInline):
    model = Comment
    fk_name = 'blog'
    extra = 0

class PointInline(admin.StackedInline):
    model = Point
    fk_name = 'blog'
    extra = 0

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_type', 'username', 'get_full_name', 'is_superuser', 'last_login']
    list_filter = ['user_type', 'is_superuser']
    search_fields = ('username', )
    inlines = []

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    get_full_name.short_description = 'Full Name'

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj:
            if obj.user_type == 'author':
                inline_instances.append(AuthorProfileInline(self.model, self.admin_site))
            elif obj.user_type == 'reader':
                inline_instances.append(ReaderProfileInline(self.model, self.admin_site))
        return inline_instances

class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_profile_image', 'get_full_name', 'country_flag', 'status']
    list_filter = ['status', 'country']
    inlines = [BlogInline]

    def show_profile_image(self, obj):
        return mark_safe(f'<img src="{obj.profile_image.url}" style="width: 150px; height: auto; border-radius: 10px;" />')
    show_profile_image.short_description = 'Profile Image'
    
    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    get_full_name.short_description = 'Full Name'

    def country_flag(self, obj):
        return format_html(
            "<img src='{}' style='height: 20px;'/>", obj.country.flag
        )
    country_flag.short_description = 'Country'

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False
    
class ReaderProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user_name', 'country_flag']
    list_filter = ['country']
    
    def get_user_name(self, obj):
        return f'{obj.user.username}'
    get_user_name.short_description = 'Full Name'

    def country_flag(self, obj):
        return format_html(
            "<img src='{}' style='height: 20px;'/>", obj.country.flag
        )
    country_flag.short_description = 'Country'

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    inlines = [SubCategoryInline]

class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'show_cover_image', 'filtered_title', 'get_author', 'get_sub_categories', 'comments_count', 'status']
    list_filter = ['status']
    search_fields = ['title', 'body']
    inlines = [CommentInline, PointInline]

    def show_cover_image(self, obj):
        return mark_safe(f'<img src="{obj.cover_image.url}" style="width: 150px; height: auto; border-radius: 10px;" />')
    show_cover_image.short_description = 'Cover Image'

    def filtered_title(self, obj):
        return f'{obj.title[:15]}{"..." if len(obj.title) > 15 else ""}'
    filtered_title.short_description = 'Title'

    def get_author(self, obj):
        return f'{obj.author.user.get_full_name()}'
    get_author.short_description = 'Author'

    def get_sub_categories(self, obj):
        return ", ".join([f'{sub_category.title} ({sub_category.category})' for sub_category in obj.sub_categories.all()])
    get_sub_categories.short_description = 'Sub Categories'

    def comments_count(self, obj):
        return obj.blog_comments.count()
    comments_count.short_description = 'Comments Count'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'commenter', 'filtered_body', 'status']
    list_filter = ['status']

    def filtered_body(self, obj):
        return f'{obj.body[:15]}{"..." if len(obj.body) > 15 else ""}'
    filtered_body.short_description = 'Comment'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AuthorProfile, AuthorProfileAdmin)
admin.site.register(ReaderProfile, ReaderProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)