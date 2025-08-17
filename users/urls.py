from django.urls import path
from .views import RegisterApi,LoginApi,LogoutApi,ProfilApi

urlpatterns = [
    path("register/",RegisterApi.as_view()),
    path("login/", LoginApi.as_view()),
    path('logout/',LogoutApi.as_view()),

    path("profil/",ProfilApi.as_view()),
]