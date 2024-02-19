from typing import Any
from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Collection, Order, OrderItem, Customer, Product, Promotion
list_of_models = [Order, OrderItem, Promotion]
admin.site.register(list_of_models)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    # making the return value to be link that naviage to product
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + 'collection_id={}'.format(collection.id))
        return format_html('<a href = "{}">{}</a>', url, collection.products_count)

    # customizing get_queryset by annotating products_count column
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))
# Adding new column to the list page


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    ordering = ['inventory']
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 15
    ordering = ['first_name', 'last_name']

    def orders(self, customer):
        return customer.orders

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(orders=Count('order'))
