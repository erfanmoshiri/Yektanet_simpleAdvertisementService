from django.urls import path

from account_management.views import Register_Users, login_user, UserViewSet

# urlpatterns = [
#     path('signup', Register_Users.as_view()),
#     path('login', login_user.as_view()),
#
# ]

# from views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls