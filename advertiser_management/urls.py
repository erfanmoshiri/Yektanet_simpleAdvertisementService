from django.urls import path
from advertiser_management.views import CreateAdv, CreateAd

urlpatterns = [
    path('advertiser', CreateAdv.as_view()),
    path('ad', CreateAd.as_view()),
]
