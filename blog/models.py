from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

from django_countries.fields import CountryField
from autoslug import AutoSlugField

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('author', 'Author'),
        ('reader', 'Reader'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='admin')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.user_type}: {self.username}'

class AuthorProfile(models.Model):
    STATUS_CHOICES = (
        ('1', 'Awaiting confirmation'),
        ('2', 'Confirmed'),
        ('3', 'Rejection confirmed'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='author_profile', editable=False)
    profile_image = models.ImageField(upload_to='author_image/')
    country = CountryField(blank_label='(select country)')
    phone_number = models.CharField(
        max_length=10,
        help_text='9123456789',
        validators=[RegexValidator(r'^\d{10}$', message='Mobile number must be 10 digits long and without leading zeros')]
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f'{self.user.username} profile'

class ReaderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='reader_profile', editable=False)
    country = CountryField(blank_label='(select country)')

    def __str__(self):
        return f'{self.user.username} profile'

class Category(models.Model):
    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_sub_categories')
    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return f'{self.title} ({self.category})'
    
    class Meta:
        verbose_name = 'sub category'
        verbose_name_plural = 'sub categories'

class Blog(models.Model):
    STATUS_CHOICES = (
        ('1', 'Awaiting confirmation'),
        ('2', 'Confirmed'),
        ('3', 'Rejection confirmed'),
    )

    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE, related_name='author_blogs')
    sub_categories = models.ManyToManyField(SubCategory, related_name='sub_categories_blogs')
    cover_image = models.ImageField(upload_to='blog_image/')
    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='title', unique=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f'{self.title[:15]}{"..." if len(self.title) > 15 else ""} by {self.author.user.get_full_name()}'

class Comment(models.Model):
    STATUS_CHOICES = (
        ('1', 'Awaiting confirmation'),
        ('2', 'Confirmed'),
        ('3', 'Rejection confirmed'),
    )

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comments')
    comment_parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comment_parent_comments', null=True, blank=True)
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comments')
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f'{self.body[:15]}{"..." if len(self.body) > 15 else ""} by {self.commenter.username}'

class Point(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_points')
    star = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    pointer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_points')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(star__gte=1, star__lte=5),
                name='valid_star_range'
            ),
            models.UniqueConstraint(fields=['blog', 'pointer'], name='unique_point_per_user')
        ]

    def __str__(self):
        return f'{self.star} star by {self.pointer.username}'
