from django.urls import URLPattern, path
from users import views

app_name ='users'

urlpatterns: list[URLPattern] = [
    path('login', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profil_user/', views.profil_user, name='profil_user'),
    path('users-cart', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),
]