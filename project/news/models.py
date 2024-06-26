from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse_lazy


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get("postRating")

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get("commentRating")
        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'

    CATEGORY_POST = [
        (NEWS, 'новость'),
        (ARTICLE, 'статья')
    ]
    category_type = models.CharField(max_length=2, choices=CATEGORY_POST, default=NEWS)
    time_in = models.DateTimeField(auto_now_add=True, )
    post_category = models.ManyToManyField(Category, through='PostCategory')
    titl = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return reverse_lazy('the_post', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.post_category}'


class PostCategory(models.Model):
    _post = models.ForeignKey(Post, on_delete=models.CASCADE)
    _category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    comUser = models.ForeignKey(User, on_delete=models.CASCADE)
    comText = models.CharField(max_length=256, null=False)
    comTime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
