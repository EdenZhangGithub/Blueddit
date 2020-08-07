from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Community(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

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
        return reverse('post', kwargs={'pk': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def get_absolute_url(self):
        return reverse('profile', args=(self.user.username,))

