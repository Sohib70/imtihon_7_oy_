from django.urls import path
from .views import OrderCreate, OrderList, OrderDetail, OrderStatusUpdate, OrderCancel


urlpatterns = [
    path('create/', OrderCreate.as_view()),
    path('list/', OrderList.as_view()),
    path('detail/<int:pk>/', OrderDetail.as_view()),
    path('update/<int:pk>/', OrderStatusUpdate.as_view()),
    path('cancel/<int:pk>/', OrderCancel.as_view()),
]