from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime, date


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name='watchlisted')

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    starting_bid = models.FloatField(null=True, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="listings_img")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="1", related_name ='listings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_timestamp = models.DateTimeField(default=datetime.now())
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    comment = models.CharField(max_length=2024)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(default=datetime.now())
    

class Bid(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return f"${self.bid}"
