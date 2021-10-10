from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from advertiser_management.forms import CreateAdForm, CreateAdvForm, CreateAdForm1
from advertiser_management.models import Ad


class CreateAdv(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')

    def post(self, request):
        form = CreateAdvForm(request.POST)
        if form.is_valid():
            adv = form.save()


class CreateAd(View):
    def get(self, request):
        # <view logic>
        # return render(request, 'add_ad_form.html')
        form = CreateAdForm1()
        return render(request, 'add_ad_form.html', {'form': form})

    def post(self, request):
        form = CreateAdForm1(request.POST)
        if form.is_valid():
            form.save()
            # ad = Ad()
            # ad.AdvertiserId = form.cleaned_data['Adv_Id']
            # ad.Link = form.cleaned_data['Link']
            # ad.Title = form.cleaned_data['Title']
            # ad.Image = form.cleaned_data['Image']
            # ad.save()
            return HttpResponse({"Done"})
        else:

            return HttpResponse(form.errors)


class Click(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')


class ShowAdds(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')
