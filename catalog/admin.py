from django.contrib import admin
from catalog.models import Genres, Languages, Publishers, Products, Comment


# admin.site.register(Genres)
# admin.site.register(Products)

@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', ) }
    list_display = ['title', ]

@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ) }

@admin.register(Publishers)
class PublishersAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ) }

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', ) }
    list_display = ['title', 'language', 'price', 'discount', 'age_limit']
    list_editable = ['discount']
    search_fields = ['title', 'discount', 'age_limit']
    list_filter = ['quantity', 'discount', 'language', 'genre']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at', 'body']
   
