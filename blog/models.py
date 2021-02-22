from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, 
                            on_delete = models.CASCADE, 
                            related_name='posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='published')
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    objects = models.Manager()
    published = PublishedManager()
    


    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year,
                                            self.publish.month,
                                            self.publish.day,
                                            self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'