from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    """
    Returns a dictionary of all categories and the current selected category.
    """
    return {'categories': Category.objects.all(), 'current_category': current_category}
