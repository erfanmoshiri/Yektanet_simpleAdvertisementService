from django.db import models

class Advertiser(models.Model):

    Name = models.CharField(max_length=30)
    # Clicks = models.IntegerField(null=True, default=0)
    # Views = models.IntegerField(null=True, default=0)


class Ad(models.Model):
    AdvertiserId = models.CharField(max_length=30)
    Title = models.CharField(max_length=30)
    Link = models.TextField()
    Image = models.ImageField(upload_to='images/')
    Approve = models.BooleanField(default=False)
    # Clicks = models.IntegerField(null=True, default=0)
    # Views = models.IntegerField(null=True, default=0)
    def __str__(self):
        return self.Title

class View(models.Model):
    AdId = models.CharField(max_length=40)
    IpAddress = models.CharField(max_length=30)
    CreatedAt = models.DateTimeField()

class Click(models.Model):
    AdId = models.CharField(max_length=40)
    IpAddress = models.CharField(max_length=30)
    CreatedAt = models.DateTimeField()