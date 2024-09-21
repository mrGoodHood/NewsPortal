from django import forms
from .models import Post, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'categories', 'title', 'text']

class FilterForm(forms.Form):
    title = forms.ModelChoiceField(
        queryset=Post.objects.values_list('title', flat=True).distinct(),
        required=False,
        label='Название',
        widget=forms.Select(attrs={'placeholder': 'Название'})
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        label='Автор',
        widget=forms.Select(attrs={'placeholder': 'Автор'})
    )
    date_after = forms.DateField(
        required=False,
        label='Дата после',
        widget=forms.DateInput(attrs={'type': 'date'})  # Виджет для выбора даты
    )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        common_group, created = Group.objects.get_or_create(name='common')
        user.groups.add(common_group)
        self.send_welcome_email(user)
        return user

    def send_welcome_email(self, user):
        subject = "Добро пожаловать на наш портал новостей!"
        html_message = render_to_string('email_welcome.html', {
            'username': user.username,
            'activation_link': f"{settings.SITE_URL}/accounts/confirm-email/"
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=html_message,
        )