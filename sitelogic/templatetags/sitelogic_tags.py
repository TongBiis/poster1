from django import template
from sitelogic.models import *

register = template.Library()


@register.simple_tag()
def get_cats():
    return PostCategory.objects.all()
