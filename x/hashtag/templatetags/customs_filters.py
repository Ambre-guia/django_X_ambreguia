from django import template
import urllib.parse

register = template.Library()

@register.filter
def starts_with(value, arg):
    return str(value).startswith(arg)

@register.filter
def clean_hashtag(word):
    if word.startswith('#'):
        return urllib.parse.quote(word[1:])  # Supprime le # et encode proprement le reste
    return word
