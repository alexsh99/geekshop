from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def basket(request):
    context = {
        'basket_items': Basket.objects.filter(user=request.user).order_by('product__category'),
        'title': 'Корзина'
    }
    return render(request, 'basket.html', context=context)


@login_required
def basket_add(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=pk)
        basket = Basket.objects.filter(user=request.user, product=product).first()
        if not basket:
            basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(id=int(pk))

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
        content = {
            'basket_items': basket_items
        }
        result = render_to_string('includes/inc_basket_list.html', content)
        cart = f"{basket_items[0].total_quantity} шт.  {basket_items[0].total_cost:.2f} руб."
        return JsonResponse({'result': result, 'cart': cart})
