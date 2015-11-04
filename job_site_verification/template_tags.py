__author__ = 'boredom23309'
from django.template.defaulttags import register

@register.filter
def get(dictionary, key):
    return dictionary.get(key)