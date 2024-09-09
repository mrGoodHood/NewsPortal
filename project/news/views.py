from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment, Author, Category
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from datetime import datetime


class NewsList(ListView):
    """Представление для списка статей"""
    model = Post
    template_name = 'news.html'
    # queryset = Post.objects.filter()
    context_object_name = 'news'
    ordering = ['-created_at']
    paginate_by = 10  # пагинация

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context

class NewsDetail(DetailView):
    """Представление для детального отображения статьи"""
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class NewsCreate(CreateView):
    """Представление для создания новой статьи"""
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')

    def form_valid(self, form):
        form.instance.post_type = 'NW'  # Устанавливаем тип как новость
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    """Представление для обновления статьи"""
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')


class NewsDelete(DeleteView):
    """Представление для удаления статьи"""
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news')  # перенаправление после удаления


class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')

    def form_valid(self, form):
        form.instance.post_type = 'AR'  # Устанавливаем тип как статья
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news')


def news_search(request):
    filterset = PostFilter(request.GET, queryset=Post.objects.all())
    news = filterset.qs

    context = {
        'filterset': filterset,
        'news': news,
    }
    return render(request, 'news_search.html', context)
