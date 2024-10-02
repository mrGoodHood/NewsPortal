# На Windows нужно запустить в разных терминалах:
# cd np && celery -A np worker -l INFO --pool=solo
# cd np && celery -A np beat -l INFO
# Перед этим в отдельном терминале запустить сервер
# Redis (если установлен локально): redis-server
import datetime
from datetime import timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category


@shared_task
def notify_subscribers(post_pk):
    """
    Если пользователь подписан на какую-либо категорию, то, как только в неё
    добавляется новая статья, её краткое содержание приходит пользователю на
    электронную почту, которую он указал при регистрации
    """

    post = Post.objects.get(pk=post_pk)
    subscribers = set()
    [subscribers.update(set(category.subscribers.all())) for category in post.category.all()]
    for user in subscribers:
        text_content = (f'Здравствуй, @{str(user)}. '
                        f'Новая статья в твоём любимом разделе!\n'
                        f'{post.title}\n{post.text[:50]}\n'
                        f'http://127.0.0.1:8000{post.get_absolute_url()}')
        html_content = render_to_string('email/new_post.html',
                                        {'post': post, 'user': user})
        email = EmailMultiAlternatives(subject=post.title,
                                       body=text_content,
                                       to=(user.email,))
        email.attach_alternative(html_content, 'text/html')
        email.send()


@shared_task
def weekly_digest():
    """
    Если пользователь подписан на какую-либо категорию, то каждый
    понедельник в 8:00 утра ему приходит на почту список новых статей,
    появившийся за неделю с гиперссылкой на каждую из них
    """

    mailing = dict()
    week_ago = datetime.now() - timedelta(days=7)
    base_url = 'http://127.0.0.1:8000'

    for category in Category.objects.all():
        posts = Post.objects.filter(category=category,
                                    created_at__gte=week_ago)
        if len(posts) != 0:
            for user in category.subscribers.all():
                mailing.setdefault(user, set())
                mailing[user].update(posts)

    for user, posts in mailing.items():
        post_list = '\n'.join([f'{post}: {base_url}{post.get_absolute_url()}' for post in posts])
        text_content = (f'Здравствуй, @{str(user)}. '
                        f'Новое за прошедшую неделю:\n'
                        f'{post_list}')
        html_content = render_to_string('email/weekly_digest.html',
                                        {'posts': posts, 'user': user})
        email = EmailMultiAlternatives(subject='Еженедельный Дайджест',
                                       body=text_content,
                                       to=(user.email,))
        email.attach_alternative(html_content, 'text/html')
        email.send()
