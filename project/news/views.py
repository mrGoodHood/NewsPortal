from lib2to3.fixes.fix_input import context

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment, Author, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm
from datetime import datetime


class NewsList(ListView):
    """Представление для списка статей"""
    model = Post
    template_name = 'news.html'
    # queryset = Post.object.filter()
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
    pk_url_kwarg = 'id'


class PostCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания новой статьи"""
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для обновления статьи"""
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления статьи"""
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')  # перенаправление после удаления


def add_comment(request, pk):
    """Представление для добавления комментария"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'news/add_comment.html', {'form': form})
