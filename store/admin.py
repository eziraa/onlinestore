from django.contrib import admin
from .models import Collection, Order, OrderItem, Customer, Product, Promotion
list_of_models = [Collection, Order, OrderItem, Customer, Product, Promotion]
admin.site.register(list_of_models)
