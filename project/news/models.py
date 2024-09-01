from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        article_ratings = self.post_set.aggregate(total=models.Sum('rating'))['total'] or 0
        article_ratings *= 3
        comment_ratings = self.user.comment_set.aggregate(total=models.Sum('rating'))['total'] or 0
        article_comments_ratings = models.Sum(models.F('rating'))
        article_comments_ratings = models.Sum(
            models.Case(
                models.When(post__author=self, then='rating'),
                output_field=models.IntegerField()
            )
        )
        self.rating = article_ratings + comment_ratings + article_comments_ratings
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}: {self.text}'


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_length = 124
        if len(self.text) > preview_length:
            return self.text[:preview_length] + '...'
        return self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
