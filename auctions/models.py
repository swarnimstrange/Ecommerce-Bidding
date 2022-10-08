from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=128)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    category = models.CharField(max_length=32, blank=True)
    closed = models.BooleanField(default=False)

class Bid(models.Model):
    bid_price = models.IntegerField(blank=True, null=True)
    bid_on = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, blank=True, null=True)
    bid_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    current_highest = models.BooleanField(default=True)

class Comment(models.Model):
    comment = models.CharField(max_length=256)
    comment_on = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, blank=True, null=True)
    comment_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

class Wishlist(models.Model):
    product = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, blank=True, null=True)
    wishlist_of = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

