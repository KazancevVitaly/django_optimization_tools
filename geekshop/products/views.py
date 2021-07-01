from django.shortcuts import render

from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime


# функции = контроллер
def index(request):
    context = {
        'title': 'GeekShop главная',
        'header': 'GeekShop Store',
        'date': datetime.datetime.now()
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        'title': 'GeekShop - Каталог',
        'header': 'GeekShop',
        'categories': ProductCategory.objects.all(),
        'date': datetime.datetime.now()
    }

    """
    context.update({
        'products': Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    })
   
    if category_id:
        # context['products'] = Product.objects.filter(category=ProductCategory.objects.get(id=category_id))
        context['products'] = Product.objects.filter(category_id=category_id)
    else:
        context['products'] = Product.objects.all()
    оставил в комментарий как вариант
    """

    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    paginator = Paginator(products, 3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)

