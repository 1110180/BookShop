from django.utils.http import urlencode
from django import template
from catalog.models import Genres

register = template.Library()

@register.simple_tag()
def tag_genres():
    return Genres.objects.all()

@register.simple_tag(takes_context=True)
def chang_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
