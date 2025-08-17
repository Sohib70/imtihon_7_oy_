from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

@admin.register(Order)
class OrderaAdmin(admin.ModelAdmin):
    list_display = ['user','status']
    list_filter = ['status', ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','amount']
    list_filter = ['product', ]
