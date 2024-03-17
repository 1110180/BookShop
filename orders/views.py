from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
import telebot

@login_required
def create_order(req):
    initial = {
        "first_name": req.user.first_name,
        "last_name": req.user.last_name,
    }

    if req.method == "POST":
        form = CreateOrderForm(data=req.POST, initial=initial)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = req.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data["phone_number"],
                            requires_delivery=form.cleaned_data["requires_delivery"],
                            address=form.cleaned_data["address"],
                            payment_on_get=form.cleaned_data["payment_on_get"],
                        )
                        # создать заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.title
                            price = cart_item.products_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f"Недостаточное количество товаров {name} на складе. В наличии - {product.quantity}"
                                )

                            new_order_item = OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            
                            product.quantity -= quantity
                            product.save()
                            

                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()
                        telegram(new_order_item)

                        messages.success(req, "Заказ оформлен!")
                        return redirect("user:profil_user")
            except ValidationError as e:
                messages.success(req, str(e))
                return redirect("users:users_cart")

    else:
        form = CreateOrderForm(initial=initial)

    context = {
        "title": "HOME-Оформление заказа",
        "form": form,
        "order": True,
    }

    return render(req, "orders/create_order.html", context=context)


def telegram(new_order_item):
    chat = '805774017'
    message = f"{new_order_item.order.user.username} заказ в обработке. Прошу ожидать готовности!"
    # message = f"{new_order_item.order.user.username} {new_order_item.order} {new_order_item.product}"
    bot = telebot.TeleBot('6293182974:AAHmAzvlIPtnFgaAsBcJ0oES91Dj8uBLMuY')
    bot.send_message(chat, 'Ваш заказ')
    bot.send_message(chat, message)




# def create_order(req):

#     if req.method == 'POST':
#         form = CreateOrderForm(data=req.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = req.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if cart_items.exists():
#                         # создать заказ
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data['phone_number'],
#                             requires_delivery=form.cleaned_data['requires_delivery'],
#                             address=form.cleaned_data['address'],
#                             payment_on_get=form.cleaned_data['payment_on_get'],
#                         )
#                         # создать заказанные товары
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.title
#                             price = cart_item.product.calculate_price()
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise ValidationError(f'Недостаточное количество товаров {name} на складе\
#                                                       В наличии - {product.quantity}')

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#                             product.quantity -= quantity
#                             product.save()

#                         # Очистить корзину пользователя после создания заказа
#                         cart_items.delete()

#                         messages.success(req, 'Заказа оформлен!')
#                         return redirect('user:profil_user')
#             except ValidationError as e:
#                 messages.success(req, str(e))
#                 return redirect('cart:order')

#     else:
#         initial = {
#             'first_name': req.user.first_name,
#             'last_name': req.user.last_name,
#         }

#     form = CreateOrderForm(initial=initial)

#     context = {
#         'title': 'HOME-Оформление заказа',
#         'form': form,
#     }

#     return render(req, 'orders/create_order.html', context=context)
