from django.db import models
from user.models import User


# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def blog_count(self):
        return self.blog_set.count()

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=25)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
