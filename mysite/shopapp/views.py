from timeit import default_timer
from django.contrib.auth.models import Group
from .models import Product, Order
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse


def shop_index(request: HttpRequest):
    reverse("shopapp:products_list")
    reverse("shopapp:orders_list")

    return render(request, 'shopapp/shop-index.html')


def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shopapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)
