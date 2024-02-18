from django.contrib import admin
from .models import Collection, Order, OrderItem, Customer, Product, Promotion
list_of_models = [Collection, Order, OrderItem, Promotion]
admin.site.register(list_of_models)

# Adding new column to the list page


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 10

    def inventory_status(self, product):
        if product.inventory <= 10:
            return 'Low'
        else:
            return 'Ok'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 15
    ordering = ['first_name', 'last_name']
