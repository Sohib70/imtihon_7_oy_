from django.urls import path
from .views import AvtotovarListCreate,AvtotovarDetailUpdateDelete

urlpatterns = [
    path("",AvtotovarListCreate.as_view()),
    path('api/<int:pk>/',AvtotovarDetailUpdateDelete.as_view())
]