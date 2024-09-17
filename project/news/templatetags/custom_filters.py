from django import template

register = template.Library()

# Список нежелательных слов
UNWANTED_WORDS = ['тренинг', 'коуч', 'инсайд', 'челендж']

@register.filter(name='censor')
def censor(text):
    for word in UNWANTED_WORDS:
        # Замена нежелательных слов на символы *
        text = text.replace(word, '*' * len(word))
        # Замена слов с первой заглавной буквой
        text = text.replace(word.capitalize(), '*' * len(word))
    return text


@register.filter
def is_author(user):
    return user.groups.filter(name='authors').exists()