from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Sum

# Create your models here.

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_post = Post.objects.filter(author=self).aggregate(Sum("rating"))
        rating_post_comment = Comment.objects.filter(user=self.author).aggregate(Sum("rating"))
        rating_comment = Comment.objects.filter(post__author=self).aggregate(Sum("rating"))

        #rating_post = self.post_set.all().aggregate(Sum("rating"))
        #rating_post_comment = self.author.comment_set.all().aggregate(Sum("rating"))
        #rating_comment = Comment.objects.filter(post__author=self).values("rating").aggregate(Sum("rating"))

        self.rating = rating_post["rating__sum"] * 3 + rating_post_comment["rating__sum"] + rating_comment["rating__sum"]
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=255, primary_key=True)

class Post(models.Model):
    TYPES = [
        ('article', 'статья'),
        ('news', 'новости')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=7, choices=TYPES, default='article')
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    post_text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.post_text[:124]}..."

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()