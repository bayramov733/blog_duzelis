from django import template
from django.template.defaultfilters import stringfilter
from posts.models import Category
import markdown as md

###########
from django.utils.safestring import mark_safe
import re
##################


register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.simple_tag
def get_categories():
    return Category.objects.all()[0:3]

##############################################
@register.filter(needs_autoescape=False)
def highlight(text, search):
    if not search:
        return text
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda m: f'<mark class="bg-yellow-300 px-1 rounded">{m.group()}</mark>',
        str(text)
    )
    return mark_safe(highlighted)
########################################################