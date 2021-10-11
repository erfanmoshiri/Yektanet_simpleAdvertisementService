import json
from datetime import datetime
from statistics import mean

from django.db.models import *
from django.db.models.functions import TruncHour
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from advertiser_management import models
from advertiser_management.forms import CreateAdvForm, CreateAdForm1, ShowAdsDto, ClickViewRelevance
from advertiser_management.models import Ad, Advertiser, Click


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CreateAdv(View):
    def get(self, request):
        form = CreateAdvForm()
        return render(request, 'add_adv_form.html', {'form': form})

    def post(self, request):
        form = CreateAdvForm(request.POST)
        if form.is_valid():
            adv = form.save()
            return HttpResponse("Created")

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
            # return HttpResponse({"Done"})
            return redirect('show')

        else:

            return HttpResponse(form.errors)


class Clicks(View):
    def get(self, request, Id):
        ad = Ad.objects.get(id=Id)
        click = Click(AdId=Id, IpAddress=request.ipAddress, CreatedAt=datetime.now())
        click.save()

        return redirect(ad.Link)


class ShowAdds(View):
    def get(self, request):
        all_ads = list(Ad.objects.all())
        all_advs = list(Advertiser.objects.all())
        # advIds = (x.AdvertiserId for x in allAds)
        # uniqueAdvIds = set(advIds)
        # ip = get_client_ip(request)
        views_list = []
        grouped_by_adv = {}
        for ad in all_ads:
            # ad.Views += 1
            # ad.save()
            views_list.append(models.View(AdId=ad.id, IpAddress=request.ipAddress, CreatedAt=datetime.now()))
            advName = [x.Name for x in all_advs if str(x.id) == ad.AdvertiserId][0]
            # advGroup = [x.get(advName) for x in groupedByAdv]
            group = grouped_by_adv.get(advName)
            if group is None:
                grouped_by_adv[advName] = [ad]
            else:
                grouped_by_adv[advName].append(ad)

        models.View.objects.bulk_create(views_list)
        final_list = []
        for k, v in grouped_by_adv.items():
            final_list.append(ShowAdsDto(k, v))

        context = {'advertisers': final_list}
        return render(request, 'ads.html', context=context)
        # return HttpResponse(groupedByAdv)


class Data(View):
    def get(self, request, id):
        final_result = {}
        d = Ad.objects.values('AdvertiserId').annotate(dcount=Count('AdvertiserId'))
        all_clicks = Click.objects.filter(AdId=id).values()
        click_count = all_clicks.count()
        all_views = models.View.objects.filter(AdId=id).values()
        view_count = all_views.count()

        final_result['click_count'] = click_count
        final_result['view_count'] = view_count

        view_time_count = models.View.objects.filter(AdId=id).annotate(hour=TruncHour('CreatedAt')).values(
            'hour').annotate(count=Count('hour'))
        click_time_count = Click.objects.filter(AdId=id).annotate(hour=TruncHour('CreatedAt')).values('hour').annotate(
            count=Count('hour'))
        click_view_relevance = click_count / view_count
        sorted_relevance_by_hour = []
        for i in view_time_count:
            clicks = 0
            for y in click_time_count:
                if i['hour'] == y['hour']:
                    clicks = y['count']
                    break

            sorted_relevance_by_hour.append(ClickViewRelevance(str(i['hour']).split('+')[0], clicks))
        sorted_relevance_by_hour.sort()
        jsoned = [x.toJSON() for x in sorted_relevance_by_hour]
        final_result['sorted_relevance_by_hour'] = jsoned

        time_delta_list = []
        for i in all_views:
            for y in all_clicks:
                seconds = (y['CreatedAt'] - i['CreatedAt']).seconds
                if (i['IpAddress'] == y['IpAddress']) and (seconds < 300):
                    time_delta_list.append(seconds)
                    break
        average_view_click_period = mean(time_delta_list)
        final_result['average_view_click_period'] = average_view_click_period
        return HttpResponse(
            json.dumps(final_result)
        )
