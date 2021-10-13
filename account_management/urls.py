from django.urls import path

from account_management.views import Register_Users, login_user

urlpatterns = [
    path('signup', Register_Users.as_view()),
    path('login', login_user.as_view()),

]