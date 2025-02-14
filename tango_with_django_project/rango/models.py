# Import the Category model
from rango.models import Category
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    # Links UserProfile to a User instance (one-to-one)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional fields for the profile
    website = models.URLField(blank=True)  # Optional personal website
    picture = models.ImageField(upload_to='profile_images', blank=True)  # Profile picture

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

def __str__(self):
    return self.title
