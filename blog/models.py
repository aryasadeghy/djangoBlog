from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

from .search import BlogPostIndex

# Create your models here.

class PublishedManagar(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status='publish')
        return queryset


class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )
    author = models.ForeignKey(User, related_name='blogpost', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug  = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    image = models.ImageField(upload_to='post/')
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')

    objects = models.Manager()
    published = PublishedManagar()

    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.pk])

    def indexing(self):
        obj = BlogPostIndex(
            meta={'id': self.id},
            author = self.author.username,
            title = self.title,
            body = self.body,
            publish = self.publish
        )
        obj.save()
        return obj.to_dict(include_meta=True)



class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {} on {}".format(self.name, self.post)


