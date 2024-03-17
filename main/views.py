from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import Genres


def index(req):
    # genres = Genres.objects.all()

    context = {
        'title': 'HOME - ГЛАВНАЯ',
        'content': 'МИР КНИГ!', 
        # 'genres': genres
    }

    return render(req, 'main/index.html', context)

def about(req):
    context = {
        'title': 'HOME - О НАС',
        'content': 'О НАС',
        'text_on_page': 'Излишне говорить, что вы лишаете себя настоящего читательского удовольствия, проходя мимо таких произведений!'
    }

    return render(req, 'main/about.html', context)

def contact(req):
    context = {
        'title': 'HOME - КОНТАКТЫ',
        'content': 'О НАС',
    }

    return render(req, 'main/contact.html', context)
