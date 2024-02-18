from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggeItem
from django.db.models import F, Func, Value
from django.db.models.aggregates import Avg, Count
from django.db.models.functions import Concat
from django.db.models.functions.math import Sqrt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db import connection


def index(request):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM store_product')
    queryset = cursor.fetchall()
    cursor.close()
    return render(request, 'index.html', {'name': 'Ezira', 'orders': list(queryset)})
