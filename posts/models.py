from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from iexfinance.stocks import Stock as IexStock

from decimal import Decimal

# Create your models here.
class Community(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "communities"

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('community', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.community.slug, 'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=100, blank=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def get_absolute_url(self):
        return reverse('profile', args=(self.user.username,))


class Stock(models.Model):
    ticker = models.CharField(max_length=5, blank=True, unique=True)
    owners = models.ManyToManyField(User, through='share')

    def __str__(self):
        return self.ticker

    def get_price(self):
        return IexStock(self.ticker).get_price()

class Share(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    def get_value(self):
        return round(Decimal(self.stock.get_price()) * self.quantity, 2)








