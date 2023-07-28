from django import template

from products.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return context
