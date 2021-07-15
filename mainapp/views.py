import random
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from .models import ProductCategory
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)


def get_related(select_product):
    return Product.objects.filter(category=select_product.category).exclude(id=select_product.id)[:3]


@login_required
def products(request, index=None, page=1):
    if index is not None and index != 0:
        category = get_object_or_404(ProductCategory, id=index)
        products_list = Product.objects.filter(category_id=index, is_active=True).order_by('price')
    else:
        products_list = Product.objects.all().order_by('price')
        category = {'name': 'все', 'id': 0}

    paginator = Paginator(products_list, 4)

    try:
        paginator_page = paginator.page(page)
    except PageNotAnInteger:
        paginator_page = paginator.page(1)
    except EmptyPage:
        paginator_page = paginator.page(paginator.num_pages)

    categories = ProductCategory.objects.all()
    context = {
        'title': 'Каталог',
        'categories': categories,
        'category': category,
        'products': paginator_page,
    }
    return render(request, 'products_list.html', context=context)


@login_required
def product(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
        'categories': ProductCategory.objects.all(),
        'related': get_related(product),
        'hot': get_hot_product()
    }
    if request.is_ajax():
        return JsonResponse({'price': product.price})
    return render(request, 'products.html', context=context)
