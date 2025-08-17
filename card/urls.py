from django.urls import path
from .views import CardCreate,AddToCard,CardItemUpdate,RemoveFromCard,ClearCard

urlpatterns = [
    path("create/",CardCreate.as_view()),
    path("add/", AddToCard.as_view()),
    path("update/<int:pk>/", CardItemUpdate.as_view()),
    path('remove/<int:pk>/', RemoveFromCard.as_view()),
    path('clear/', ClearCard.as_view()),
]
