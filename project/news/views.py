from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment, Author, Category
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PostForm
from datetime import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages


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


class NewsCreate(PermissionRequiredMixin, CreateView):
    """Представление для создания новой статьи"""
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Считаем суммарное количество новостей и статей, созданных пользователем за текущие сутки
        posts_today = Post.objects.filter(
            author__user=user,
            created_at__date=now().date()  # Фильтрация по дате
        ).count()

        # Проверка: если пользователь уже создал 3 публикации за день
        if posts_today >= 3:
            # Выводим сообщение об ошибке и перенаправляем пользователя
            messages.error(self.request, "Вы не можете создавать больше трёх публикаций в день.")
            return redirect('news')  # Перенаправляем пользователя на страницу новостей

        # Если проверка пройдена, продолжаем создание новости
        form.instance.post_type = 'NW'  # Устанавливаем тип как новость
        form.instance.author = Author.objects.get(user=user)  # Устанавливаем автора
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для обновления статьи"""
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')
    permission_required = 'news.change_post'


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Представление для удаления статьи"""
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news')  # перенаправление после удаления
    permission_required = 'news.delete_post'


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        # Получаем текущего пользователя
        user = self.request.user
        # Считаем суммарное количество новостей и статей, созданных пользователем за текущие сутки
        posts_today = Post.objects.filter(
            author__user=user,
            created_at__date=now().date()  # Фильтрация по дате
        ).count()

        # Проверка: если пользователь уже создал 3 публикации за день
        if posts_today >= 3:
            # Выводим сообщение об ошибке и перенаправляем пользователя
            messages.error(self.request, "Вы не можете создавать больше трёх публикаций в день.")
            return redirect('news')  # Перенаправляем пользователя на страницу новостей

        # Если проверка пройдена, продолжаем создание статьи
        form.instance.post_type = 'AR'  # Устанавливаем тип как статья
        form.instance.author = Author.objects.get(user=user)  # Устанавливаем автора
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news')
    permission_required = 'news.change_post'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news')
    permission_required = 'news.delete_post'


@login_required
def user_profile(request):
    is_author = request.user.groups.filter(name='authors').exists()
    return render(request, 'account/user_profile.html', {
        'is_author': is_author,
    })


@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    # Проверка на принадлежность к группе
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        # Создаем объект Author для текущего юзера, если он не существует
        Author.objects.get_or_create(user=user)
    return redirect('/')


# Представление для подписки на категорию
@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.user in category.subscribers.all():
        category.subscribers.remove(request.user)  # Отписка
    else:
        category.subscribers.add(request.user)  # Подписка

    return redirect('news')  # Перенаправляем пользователя обратно на страницу новостей


def news_search(request):
    filterset = PostFilter(request.GET, queryset=Post.objects.all())
    news = filterset.qs

    context = {
        'filterset': filterset,
        'news': news,
    }
    return render(request, 'news_search.html', context)
