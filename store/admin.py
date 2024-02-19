from typing import Any
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Collection, Order, OrderItem, Customer, Product, Promotion
list_of_models = [Promotion]
admin.site.register(list_of_models)

# Creating Custom Inventory filter


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any):
        return [
            ('<10', 'Low'),
            ('else', 'Ok'),

        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == 'else':
            return queryset.filter(Q(inventory__gte=10))

        return queryset

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
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
    actions = ['clear_inventory']
    autocomplete_fields = ['collection']
    search_fields = ['title']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10

    list_filter = ['collection', 'last_update', InventoryFilter]
    ordering = ['inventory']

    def inventory_status(self, product: Product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were updated successfully',
            messages.SUCCESS
        )



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 15
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    def orders(self, customer):
        return customer.orders

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(orders=Count('order'))


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
