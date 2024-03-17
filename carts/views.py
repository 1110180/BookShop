from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from catalog.models import Products


def cart_add(request):

    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)
    

    user_carts = get_user_carts(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': user_carts}, request=request
    )

    response_data = {
        'message': 'Добавлено в корзину',
        'cart_items_html': cart_items_html,
    }

    return JsonResponse(response_data)



def cart_change(req):
    cart_id = req.POST.get("cart_id")
    quantity = req.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    cart = get_user_carts(req)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': cart}, request=req
    )

    response_data = {
        'message': 'Количество изменено',
        'cart_items_html': cart_items_html,
        'quantity_deleted': updated_quantity,
    }

    return JsonResponse(response_data)



def cart_remove(req):

    cart_id = req.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_carts = get_user_carts(req)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {'carts': user_carts}, request=req
    )

    response_data = {
        'message': 'Удалено из корзины',
        'cart_items_html': cart_items_html,
        'quantity_deleted': quantity,
    }

    return JsonResponse(response_data)