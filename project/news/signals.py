from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    """Отправка email подписчикам категории при создании новой статьи"""
    if created:
        categories = instance.categories.all()
        subscribers = set()

        for category in categories:
            subscribers.update(category.subscribers.all())

        for subscriber in subscribers:
            subject = instance.title  # Заголовок письма
            message = render_to_string('email_notification.html', {
                'username': subscriber.username,
                'title': instance.title,
                'text_preview': instance.text[:50],
                'post': instance,
            })

            # Отправляем письмо
            send_mail(
                subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                fail_silently=False,
                html_message=message
            )
