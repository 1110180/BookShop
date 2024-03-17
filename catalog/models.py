from django.db import models
from django.urls import reverse
from users.models import User

class Genres(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Жанр книги')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        ordering = ['title']
        db_table = 'genre'
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title 


class Languages(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Язык книги')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        ordering = ['name']
        db_table = 'language'
        verbose_name = 'язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return self.name


class Publishers(models.Model):
    name = models.CharField(max_length=30, verbose_name='Издательство')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        ordering = ['name']
        db_table = 'publisher'
        verbose_name = 'издательство'
        verbose_name_plural = 'Издательства'

    def __str__(self):
        return self.name 


class Authors(models.Model):
    last_name = models.CharField(max_length=300, verbose_name='ФИО автора')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    description = models.TextField(blank=True, null=True, verbose_name='Сведения об авторе')
    photo = models.ImageField(upload_to='catalog_photo', blank=True, null=True, verbose_name='Фото автора')
   

    class Meta:
        ordering = ['last_name']
        db_table = 'author'
        verbose_name = 'автор'
        verbose_name_plural = 'Авторы'
        
    def __str__(self):
        return self.last_name


class Products(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название книги')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    genre = models.ForeignKey(to=Genres, on_delete=models.CASCADE, verbose_name='Жанр книги', null=True)
    language = models.ForeignKey(to=Languages, on_delete=models.CASCADE, verbose_name='Язык книги', null=True)
    publisher = models.ForeignKey(to=Publishers, on_delete=models.CASCADE, verbose_name='Издательство', null=True)
    year_publication = models.CharField(max_length=4, verbose_name='Год издания')
    author = models.ManyToManyField(to=Authors, verbose_name='Автор(ы) книги')
    summary = models.TextField(blank=True, null=True, verbose_name='Аннотация книги')
    isbn = models.CharField(max_length=15, unique=True, verbose_name='ISBN  книги')
    image = models.ImageField(upload_to='catalog_images', blank=True, null=True, verbose_name='Изображение обложки книги')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=0, verbose_name='Скидка в %')
    quantity = models.PositiveBigIntegerField(default=0, verbose_name='Количество')
    age_limit = models.PositiveSmallIntegerField(default=0, verbose_name='Ограничение по возрасту')

    class Meta:
        ordering = ['title']
        db_table = 'product'
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        ordering = ("id",)

    def __str__(self):
        return f'{self.title} Количество - {self.quantity}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    def display_id(self):
        return f'{self.id:05}'
    
    
    def calculate_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount/100, 2)
        
        return self.price


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='ОТЗЫВ')
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'Комментарий от {self.user} к {self.product}'