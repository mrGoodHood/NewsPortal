from django.utils.timezone import now
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Post
from datetime import timedelta


def send_weekly_updates():
    """Отправляет еженедельные письма с новыми статьями подписчикам."""
    last_week = now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        posts_in_category = Post.objects.filter(categories=category, created_at__gte=last_week)

        if posts_in_category.exists():
            # Собираем всех подписчиков категории
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                # Создаем контекст для письма
                message = render_to_string('weekly_email.html', {
                    'username': subscriber.username,
                    'posts': posts_in_category,
                    'category': category,
                })

                # Отправляем письмо
                send_mail(
                    subject=f"Новые статьи в разделе {category.name}",
                    message='',  # Пустое текстовое сообщение
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                    html_message=message  # Используем HTML-версию письма
                )
