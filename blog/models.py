from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    author = models.CharField(max_length=150)
    slug = models.CharField(max_length=120, default='')
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return "Comment by- " + str(self.user)
