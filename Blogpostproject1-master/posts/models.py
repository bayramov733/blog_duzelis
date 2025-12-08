from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def _str_(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def _str_(self):
        return self.title
    
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def _str_(self):
        return self.title


##############################################

class AboutPage(models.Model):
    title = models.CharField(max_length=100, default="About Me")
    content = models.TextField()
    author_name = models.CharField(max_length=50)
    author_role = models.CharField(max_length=50)
    
    def _str_(self):
        return self.title
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"