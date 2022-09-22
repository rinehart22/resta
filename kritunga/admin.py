from django.contrib import admin
from kritunga.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Chef)
admin.site.site_header='DataFlair'




@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [ 'location_name','available']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user','product_name', 'description',
                    'price',  'category_name', 'created_at','prepared_by','checkout_status']




@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'description',
                    'product_price', 'product_image', 'category']
