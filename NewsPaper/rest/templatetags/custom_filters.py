from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    bad_words = {'Динамо': 'Зенит', 'запретит': '***', 'запрет': '***'}
    for i, j in bad_words.items():
        value = value.replace(i, j)
    return value