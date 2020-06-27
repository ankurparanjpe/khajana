from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.ForeignKey('blog.SubTitle',related_name='subtitle',on_delete=models.CASCADE,default=1)
    text = models.TextField()
    create_date = models.DateTimeField(blank=True, default=timezone.now)
    pic = models.ImageField(blank=True, default="default.jpeg")
    video = EmbedVideoField(blank=True)

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=150)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail')

    def __str__(self):
        return self.text


class Subtitle(models.Model):
    subs = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.subs


class City(models.Model):
    city = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('weather')

    def __str__(self):
        return self.city
