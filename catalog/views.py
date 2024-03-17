from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator
from catalog.models import Authors, Products, Comment
from catalog.utils import q_search
from django.shortcuts import render
from .forms import CommentForm
from .models import Comment


def catalog(req, genre_slug=None):

    page = req.GET.get('page', 1)
    sale = req.GET.get('sale', None)
    order = req.GET.get('order', None)
    age_limit = req.GET.get('age_limit', None)
    query = req.GET.get('q', None)

    if genre_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(genre__slug=genre_slug))
    

    if sale:
        goods = goods.filter(discount__gt=0)
    if order and order != 'default':
        goods = goods.order_by(order)
    if age_limit:
        goods = goods.filter(age_limit=age_limit)


    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))


    context = {
        "title": "HOME - КАТАЛОГ",
        "goods": current_page, 
        'slug_url': genre_slug,
    }

    return render(req, "catalog/catalog.html", context)



def proverkaComm(newcom):
    blacklist = ['жопа', 'херня',]
    spisok = newcom.body.lower().split()

    for one in spisok:
        if one in blacklist:
            newcom.active = False
            newcom.save()
            return False

    previous_com = Comment.objects.filter(user=newcom.user).order_by('-created_at').first()
    if previous_com and previous_com.body.lower() == newcom.body.lower():
        newcom.active = False
        newcom.save()
        return False

    newcom.active = True
    newcom.save()


def product(req, product_slug):
    product = Products.objects.get(slug=product_slug)
    author = product.author.all()

    if req.method == 'POST' and req.user.is_authenticated: 
        comment_form = CommentForm(req.POST)
        if comment_form.is_valid():
            newcom = comment_form.save(commit=False)
            newcom.product = product
            newcom.user = req.user
            if proverkaComm(newcom):
                newcom.save()

    # обираем комментарии после возможного создания нового комментария
    comment = product.comment_set.filter(active=True)
    comment_form = CommentForm()  # форма была доступна только авторизованным пользователям

    context = {
        "product": product,
        'author': author,
        'comments': comment,
        'comment_form': comment_form if req.user.is_authenticated else None  
    }

    # Вывод информации
    print('Product: ', product)
    print('Authors: ', author)
    print('Comment: ', comment)
    print('Comment Form: ', comment_form)

    return render(req, "catalog/product.html", context=context)



def authors(req, authors_slug):
    authors = Authors.objects.get(slug=authors_slug)

    context = {
        "authors": authors,
    }

    return render(req, "catalog/authors.html", context=context)

















# РАБОЧИЯ ФУНКЦИЯ
# def product(req, product_slug):
#     product = Products.objects.get(slug=product_slug)

#     author = product.author.all()

#     context = {
#         "product": product,
#         'author': author
#     }

#     # Вывод информации
#     print('Product: ', product)
#     print('Authors: ', author)

#     return render(req, "catalog/product.html", context=context)





























# def proverkaComm(newcom):
#     blacklist = ['жопа', 'сука', 'херня', 'блять']
#     spisok = newcom.body.lower().split()

#     for one in spisok:
#         if one in blacklist:
#             newcom.delete()
#             return False

#     previous_com = Comment.objects.filter(user=newcom.user).order_by('-created_at').first()
#     if previous_com and previous_com.body.lower() == newcom.body.lower():
#         newcom.delete()
#         return False

#     newcom.active = True
#     newcom.save()
#     return True

# def add_comment(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             if proverkaComm(comment):
#                 return redirect('some_view')
#     else:
#         form = CommentForm()
#     return render(request, 'add_comment.html', {'form': form})

