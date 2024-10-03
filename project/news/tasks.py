from datetime import datetime, timedelta

from celery import shared_task
from celery.schedules import crontab
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from project.celery import app

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
    [subscribers.update(get_subscribers(category)) for category in post.category.all()]
    for user in subscribers:
        text_content = (f'Привет, @{str(user)}. '
                        f'Новая статья в твоём любимом разделе!\n'
                        f'{post.title}\n{post.text[:50]}\n'
                        f'http://127.0.0.1:8000{post.get_absolute_url()}')
        html_content = render_to_string('email_notification.html',
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
        text_content = (f'Привет, @{str(user)}. '
                        f'Новости за прошедшую неделю:\n'
                        f'{post_list}')
        html_content = render_to_string('email_weekly_update.html',
                                        {'posts': posts, 'user': user})
        email = EmailMultiAlternatives(subject='Еженедельное обновление',
                                       body=text_content,
                                       to=(user.email,))
        email.attach_alternative(html_content, 'text/html')
        email.send()


        # Настройка расписания задачи в Celery
        app.conf.beat_schedule = {
            'send_weekly_digest': {
                'task': 'news.tasks.weekly_digest',
                'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
            },
        }


def get_subscribers(category):
    return set(category.subscribers.all())