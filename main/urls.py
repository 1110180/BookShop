from django.urls import URLPattern, path
from main import views

app_name  ='main'

urlpatterns: list[URLPattern] = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
