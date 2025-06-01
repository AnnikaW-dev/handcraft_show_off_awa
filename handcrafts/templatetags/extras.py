from django import template
import re

register = template.Library()

@register.filter
def clean_excerpt(value):
    if not value:
        return ''

   # Ta bort alla HTML-taggar (inklusive <p>, <br>, <strong>, etc)
    value = re.sub(r'<[^>]+>', '', value)

    # Ta bort radbrytningar (från t.ex. rich text)
    value = re.sub(r'(\r\n|\n|\r)', ' ', value)

    # Ersätt flera mellanslag med ett
    value = re.sub(r'\s{2,}', ' ', value)

    return value.strip()
