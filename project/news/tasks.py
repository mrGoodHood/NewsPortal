from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category
from django.conf import settings

def send_weekly_update():
    one_week_ago = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=one_week_ago)

    if new_posts.exists():
        subscribers = set()
        for post in new_posts:
            subscribers.update(post.categories.values_list('subscribers', flat=True))

        for subscriber in subscribers:
            subject = "Еженедельное обновление: новые статьи"
            message = render_to_string('email_weekly_update.html', {
                'posts': new_posts,
                'username': subscriber.username,
            })
            send_mail(
                subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                fail_silently=False,
                html_message=message,
            )
