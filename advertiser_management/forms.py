from django import forms

from advertiser_management.models import Ad, Advertiser


# class CreateAdForm(forms.Form):
#
#     Adv_Id = forms.CharField(label='Adv_Id', max_length=100)
#     Title = forms.CharField(label='Title', max_length=100)
#     Link = forms.CharField(label='Link', max_length=1000)
#     Image = forms.ImageField(label='Image')

class CreateAdForm1(forms.ModelForm):
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
