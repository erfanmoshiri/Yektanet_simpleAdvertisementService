import json
from django import forms
from rest_framework import serializers
from advertiser_management.models import Ad, Advertiser


class CreateAdForm(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('Title', 'AdvertiserId', 'Link', 'Image')


class CreateAdvForm(forms.ModelForm):
    class Meta:
        model = Advertiser
        fields = ('Name',)


class ShowAdsDto:
    def __init__(self, name, ad):
        self.Name = name
        self.Ads = ad

    Name: str
    Ads: list


class ClickViewRelevance:
    hour: str
    count: int

    def __init__(self, hour, count):
        self.hour = hour
        self.count = count

    def __eq__(self, other):
        return self.count == other.count

    def __lt__(self, other):
        return self.count > other.count

    def __le__(self, other):
        return self.count >= other.count

    def toJSON(self):
        return {'hour': self.hour, 'count': self.count}
