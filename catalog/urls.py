from django.urls import URLPattern, path
from catalog import views

app_name  = 'catalog'

urlpatterns: list[URLPattern] = [
    path('search/', views.catalog, name='search'),
    path('<slug:genre_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path('authors/<slug:authors_slug>/', views.authors, name='authors'),
]
