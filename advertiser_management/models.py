from django.db import models

class Advertiser(models.Model):

    Name = models.CharField(max_length=30)
    Clicks = models.IntegerField(null=True, default=0)
    Views = models.IntegerField(null=True, default=0)


class Ad(models.Model):
    AdvertiserId = models.CharField(max_length=30)
    Title = models.CharField(max_length=30)
    Link = models.TextField()
    Clicks = models.IntegerField(null=True, default=0)
    Views = models.IntegerField(null=True, default=0)
    Image = models.ImageField(upload_to='images/')
    # Link = models.ImageField ? Images will be handled in another way
