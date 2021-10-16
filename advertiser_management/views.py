import json
from datetime import datetime
from statistics import mean

from django.db.models import *
from django.db.models.functions import TruncHour
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from advertiser_management import models
from advertiser_management.forms import CreateAdvForm, CreateAdForm, ShowAdsDto, ClickViewRelevance
from advertiser_management.models import Ad, Advertiser, Click


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CreateAdv(APIView):
    def get(self, request):
        return render(request, "advertiser.html", )

    def post(self, request):
        adv = CreateAdvForm(data=request.data)
        if adv.is_valid():
            adv.save()
            return Response({'message': 'advertiser added successfully!'})

        return Response({'message': adv.errors})


class CreateAd(APIView):
    def get(self, request):
        return render(request, "ad.html", )

    def post(self, request):
        ad = CreateAdForm(data=request.data)
        if ad.is_valid():
            ad.save()
            return Response({'message': 'ad added successfully!'})

        return Response({'message': ad.errors})


class Clicks(View):
    def get(self, request, Id):
        ad = Ad.objects.get(id=Id)
        click = Click(AdId=Id, IpAddress=request.ipAddress, CreatedAt=datetime.now())
        click.save()

        return redirect(ad.Link)


class ShowAdds(APIView):
    def get(self, request):
        all_ads = list(Ad.objects.all())
        all_advs = list(Advertiser.objects.all())
        views_list = []
        grouped_by_adv = {}
        for ad in all_ads:
            views_list.append(models.View(AdId=ad.id, IpAddress=request.ipAddress, CreatedAt=datetime.now()))
            advName = [x.Name for x in all_advs if str(x.id) == ad.AdvertiserId][0]
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


class Data(APIView):
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
        final_result['click_view_relevance'] = click_view_relevance

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
