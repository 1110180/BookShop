from django.db import models
from catalog.models import Products
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveBigIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')


    class Meta:
        db_table = 'cart'
        verbose_name = "корзину"
        verbose_name_plural = "корзина"

    objects = CartQueryset().as_manager()
    
    def products_price(self):
        return round(self.product.calculate_price() * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.title} | Количество {self.quantity}'
        
        return f'Анонимная корзина | Товар {self.product.title} | Количество {self.quantity}'
    


