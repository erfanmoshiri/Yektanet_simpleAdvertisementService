from django.conf.urls.static import static
from django.urls import path

from Yektanet import settings
from advertiser_management.views import CreateAdv, CreateAd, ShowAdds, Clicks, Data

urlpatterns = [
    path('advertiser', CreateAdv.as_view()),
    path('ad', CreateAd.as_view()),
    path('show', ShowAdds.as_view(), name='show'),
    path('click/<str:Id>', Clicks.as_view()),
    path('data/<str:id>', Data.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
