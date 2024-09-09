from django import forms
from .models import Post, Author

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