from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category
from django.conf import settings
from django.contrib.auth.models import User

def send_weekly_update():
    one_week_ago = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=one_week_ago)

    if new_posts.exists():
        # Получаем всех подписчиков категорий новых постов
        subscribers = set(User.objects.filter(subscriptions__post__in=new_posts).distinct())

        for subscriber in subscribers:
            # Проверяем наличие email у подписчика
            if subscriber.email:
                subject = "Еженедельное обновление: новые статьи"
                message = render_to_string('email_weekly_update.html', {
                    'posts': new_posts,
                    'username': subscriber.username,
                })
                # Отправляем письмо
                send_mail(
                    subject,
                    '',
                    settings.DEFAULT_FROM_EMAIL,
                    [subscriber.email],
                    fail_silently=False,
                    html_message=message,
                )