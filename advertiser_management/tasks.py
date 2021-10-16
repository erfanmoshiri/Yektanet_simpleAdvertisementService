from datetime import datetime
from celery import shared_task
from django.db.models import Count, Sum
from advertiser_management.models import View, Ad, Click, HourlyView, HourlyClick, DailyClick, DailyView


@shared_task
def hourly_analytics():
    now = datetime.now()
    current_hour = datetime.now().hour
    last_hour = datetime(year=now.year, day=now.day, month=now.month,
                         hour=current_hour - 1, minute=0, second=0)
    click_data = Click.objects.filter(CreatedAt__gte=last_hour).values('AdId').annotate(count=Count('AdId'))
    view_data = View.objects.filter(CreatedAt__gte=last_hour).values('AdId').annotate(count=Count('AdId'))
    clicks_data_list = [HourlyClick(ad_id=x['AdId'], count=x['count'], created_at=last_hour) for x in click_data]
    views_data_list = [HourlyView(ad_id=x['AdId'], count=x['count'], created_at=last_hour) for x in view_data]
    HourlyClick.objects.bulk_create(clicks_data_list)
    HourlyView.objects.bulk_create(views_data_list)


@shared_task()
def daily_analytics():
    now = datetime.now()
    current_day = datetime.now().day
    last_day = datetime(year=now.year, day=current_day - 1, month=now.month,
                        hour=0, minute=0, second=0)
    click_data = HourlyClick.objects.filter(created_at__gte=last_day).values('ad_id').annotate(count=Sum('ad_id'))
    view_data = HourlyView.objects.filter(created_at__gte=last_day).values('ad_id').annotate(count=Sum('ad_id'))
    click_data_list = [DailyClick(ad_id=x['ad_id'], count=x['count'], created_at=last_day) for x in click_data]
    views_data_list = [DailyView(ad_id=x['ad_id'], count=x['count'], created_at=last_day) for x in view_data]
    DailyClick.objects.bulk_create(click_data_list)
    DailyView.objects.bulk_create(views_data_list)
