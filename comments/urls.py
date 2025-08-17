from django.urls import path
from .views import CommentListCreate, CommentDetailUpdateDelete, AllComments

urlpatterns = [
    path('listcreate/<int:pk>/', CommentListCreate.as_view()),
    path('detailupdatedelete/<int:pk>/', CommentDetailUpdateDelete.as_view()),
    path('all/', AllComments.as_view()),
]