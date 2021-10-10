from django.urls import path
from advertiser_management.views import CreateAdv, CreateAd, ShowAdds, Click

urlpatterns = [
    path('advertiser', CreateAdv.as_view()),
    path('ad', CreateAd.as_view()),
    path('show', ShowAdds.as_view()),
    path('click/<str:Id>', Click),
]
