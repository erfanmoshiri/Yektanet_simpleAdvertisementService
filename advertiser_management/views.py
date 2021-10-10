from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from advertiser_management.forms import CreateAdvForm, CreateAdForm1, ShowAdsDto
from advertiser_management.models import Ad, Advertiser


class CreateAdv(View):
    def get(self, request):
        form = CreateAdvForm()
        return render(request, 'add_adv_form.html', {'form': form})

    def post(self, request):
        form = CreateAdvForm(request.POST)
        if form.is_valid():
            adv = form.save()
            return HttpResponse(f'id: {adv.id}')
        return HttpResponse("failed")


class CreateAd(View):
    def get(self, request):
        # return render(request, 'add_ad_form.html')
        form = CreateAdForm1()
        return render(request, 'add_ad_form.html', {'form': form})

    def post(self, request):
        form = CreateAdForm1(request.POST or None, request.FILES or None)
        if form.is_valid():
            # body = json.loads(request.body.decode('utf-8'))
            adv_idd = request.POST.get("AdvertiserId")
            try:
                f = Advertiser.objects.get(id=adv_idd)
                form.save()
            except:
                return HttpResponse('Advertiser were not found')

            # ad = Ad()
            # ad.AdvertiserId = form.cleaned_data['Adv_Id']
            # ad.Link = form.cleaned_data['Link']
            # ad.Title = form.cleaned_data['Title']
            # ad.Image = form.cleaned_data['Image']
            # ad.save()
            return HttpResponse({"Done"})
        else:

            return HttpResponse(form.errors)


def Click(request, Id):
    ad = Ad.objects.get(id=Id)
    ad.Clicks += 1
    ad.save()
    return redirect(ad.Link)


class ShowAdds(View):
    def get(self, request):
        allAds = list(Ad.objects.all())
        allAdvs = list(Advertiser.objects.all())
        # advIds = (x.AdvertiserId for x in allAds)
        # uniqueAdvIds = set(advIds)

        groupedByAdv = {}
        for ad in allAds:
            ad.Views += 1
            ad.save()
            advName = [x.Name for x in allAdvs if str(x.id) == ad.AdvertiserId][0]
            # advGroup = [x.get(advName) for x in groupedByAdv]
            group = groupedByAdv.get(advName)
            if group is None:
                groupedByAdv[advName] = [ad]
            else:
                groupedByAdv[advName].append(ad)

        finalList = []
        for k, v in groupedByAdv.items():
            finalList.append(ShowAdsDto(k, v))

        context = {'advertisers': finalList}
        return render(request, 'ads.html', context=context)
        # return HttpResponse(groupedByAdv)
