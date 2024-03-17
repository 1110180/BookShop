from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.shortcuts import redirect, render
from carts.models import Cart
from orders.models import Order, OrderItem
from django.db.models import Prefetch

from users.forms import UserLoginForm, UserRegistrationForm, ProfileUserForm

def login(req):
    if req.method == 'POST':
        form = UserLoginForm(data=req.POST)
        if form.is_valid():
            username = req.POST['username']
            password = req.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = req.session.session_key

            if user:
                auth.login(req, user)
                messages.success(req, f'{username}, Добро пожаловать!')

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = req.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(req.POST.get('next'))
                
                return HttpResponseRedirect(reverse('user:profil_user'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form,
    }
    
    return render(req, 'users/login.html', context)



def registration(req):
    if req.method == 'POST':
        form = UserRegistrationForm(data=req.POST)
        if form.is_valid():
            form.save()

            session_key = req.session.session_key

            user = form.instance
            auth.login(req, user)

            if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(req, f'{user.username}, Регистрация прошла успешно! ')
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    
    return render(req, 'users/registration.html', context)

@login_required
def profil_user(req):
    if req.method == 'POST':
        form = ProfileUserForm(data=req.POST, instance=req.user, files=req.FILES)
        if form.is_valid():
            form.save()
            messages.success(req, 'Данные пользователя обновлены!')
            return HttpResponseRedirect(reverse('user:profil_user'))
    else:
        form = ProfileUserForm(instance=req.user)

        orders = (
            Order.objects.filter(user=req.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )

    context = {
        'title': 'Личный кабинет',
        'form': form,
        "orders": orders,
    }
    
    return render(req, 'users/profil_user.html', context)


def users_cart(req):
    return render(req, 'users/users_cart.html')


@login_required
def logout(req):
    messages.success(req, f'{req.user.username}, До свидания!')
    auth.logout(req)
    
    return redirect(reverse('main:index'))

