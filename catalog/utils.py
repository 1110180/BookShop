import keyword
from catalog.models import Products
from django.db.models import Q


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    
    keyword = [word for word in query.split() if len(word) > 2]

    q_search = Q()

    for token in keyword:
        q_search |= Q(title__icontains=token)

    return Products.objects.filter(q_search)

